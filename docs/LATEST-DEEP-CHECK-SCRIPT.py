from __future__ import annotations

import asyncio
import inspect
import os
import struct
from pathlib import Path

import openhop_core

from openhop_core.companion.base_callbacks import _CallbackMixin
from openhop_core.companion.constants import (
    FRAME_OUTBOUND_PREFIX,
    RESP_CODE_CURR_TIME,
    RESP_CODE_STATS,
    STATS_TYPE_PACKETS,
)
from openhop_core.companion.frame_server.commands_device import _DeviceCommandsMixin
from openhop_core.companion.frame_server.push import _PushMixin
from openhop_core.companion.frame_server.server import CompanionFrameServer
from openhop_core.companion.frame_server.transport import _FrameTransportMixin
from openhop_core.companion.stats_collector import StatsCollector
from openhop_core.protocol.constants import PAYLOAD_TYPE_ACK, PH_TYPE_SHIFT, ROUTE_TYPE_FLOOD
from openhop_core.protocol.packet import Packet


class FakeWriter:
    def __init__(self) -> None:
        self.frames: list[bytes] = []
        self._closing = False

    def write(self, frame: bytes) -> None:
        self.frames.append(bytes(frame))

    async def drain(self) -> None:
        # End the writer loop immediately after the first emitted heartbeat.
        raise ConnectionResetError("test stop")

    def is_closing(self) -> bool:
        return self._closing

    def close(self) -> None:
        self._closing = True


class HeartbeatHarness(_FrameTransportMixin):
    pass


async def check_unsolicited_heartbeat() -> str:
    h = HeartbeatHarness()
    h._write_queue = asyncio.Queue()
    h._heartbeat_interval = 0.001
    h.bridge = type("Bridge", (), {"get_time": lambda self: 0x12345678})()
    writer = FakeWriter()
    await h._writer_loop(writer)
    assert len(writer.frames) == 1
    frame = writer.frames[0]
    assert frame[0] == FRAME_OUTBOUND_PREFIX
    payload_len = struct.unpack("<H", frame[1:3])[0]
    payload = frame[3:]
    assert payload_len == 5
    assert payload[0] == RESP_CODE_CURR_TIME
    assert struct.unpack("<I", payload[1:5])[0] == 0x12345678
    return frame.hex()


def check_payloadless_packet() -> tuple[bool, int, int]:
    header = (PAYLOAD_TYPE_ACK << PH_TYPE_SHIFT) | ROUTE_TYPE_FLOOD
    pkt = Packet()
    accepted = pkt.read_from(bytes([header, 0]))
    assert accepted is True
    assert pkt.payload_len == 0
    return accepted, pkt.payload_len, pkt.get_raw_length()


class StatsHarness(_DeviceCommandsMixin):
    def __init__(self, totals: dict) -> None:
        self.stats_getter = None
        self.bridge = type("Bridge", (), {"get_stats": lambda self, _stats_type: totals})()
        self.frames: list[bytes] = []

    def _write_frame(self, frame: bytes) -> None:
        self.frames.append(bytes(frame))

    def _write_err(self, _err: int) -> None:
        raise AssertionError("unexpected error frame")


async def check_packet_stats_key_mismatch() -> tuple[dict, tuple[int, ...]]:
    stats = StatsCollector()
    stats.record_tx(True)
    stats.record_tx(False)
    stats.record_rx(True)
    totals = stats.get_totals()
    assert totals["total_tx"] == 2 and totals["total_rx"] == 1
    harness = StatsHarness(totals)
    await harness._cmd_get_stats(bytes([STATS_TYPE_PACKETS]))
    frame = harness.frames[-1]
    assert frame[:2] == bytes([RESP_CODE_STATS, STATS_TYPE_PACKETS])
    values = struct.unpack("<IIIIIII", frame[2:])
    # recv and sent are zero because the encoder asks for different keys.
    assert values[0] == 0 and values[1] == 0
    assert values[2:6] == (1, 1, 1, 0)
    return totals, values


class CallbackBridge(_CallbackMixin):
    def __init__(self) -> None:
        self._push_callbacks = {
            key: []
            for key in (
                "message_event",
                "channel_message_event",
                "channel_data_event",
                "send_confirmed",
                "advert_received",
                "node_discovered",
                "contact_path_updated",
                "binary_response",
                "path_discovery_response",
                "contact_deleted",
                "contacts_full",
                "raw_data_received",
            )
        }

    def _reg(self, key, callback):
        self._push_callbacks[key].append(callback)

    on_send_confirmed = lambda self, cb: self._reg("send_confirmed", cb)
    on_advert_received = lambda self, cb: self._reg("advert_received", cb)
    on_node_discovered = lambda self, cb: self._reg("node_discovered", cb)
    on_contact_path_updated = lambda self, cb: self._reg("contact_path_updated", cb)
    on_binary_response = lambda self, cb: self._reg("binary_response", cb)
    on_path_discovery_response = lambda self, cb: self._reg("path_discovery_response", cb)
    on_contact_deleted = lambda self, cb: self._reg("contact_deleted", cb)
    on_contacts_full = lambda self, cb: self._reg("contacts_full", cb)
    on_raw_data_received = lambda self, cb: self._reg("raw_data_received", cb)


class PushHarness(_PushMixin):
    def __init__(self, bridge) -> None:
        self.bridge = bridge


def check_callback_erasure() -> tuple[int, int]:
    bridge = CallbackBridge()
    application_callback = lambda _event: None
    bridge.on_message_event(application_callback)
    before = len(bridge._push_callbacks["message_event"])
    PushHarness(bridge)._setup_push_callbacks()
    after_callbacks = bridge._push_callbacks["message_event"]
    assert before == 1
    assert application_callback not in after_callbacks
    assert len(after_callbacks) == 1  # only frame-server callback remains
    return before, len(after_callbacks)


def check_unexpired_owner_state(core_root: Path) -> tuple[bool, bool, bool]:
    transport_src = (core_root / "src/openhop_core/companion/frame_server/transport.py").read_text()
    cleanup = transport_src[transport_src.index("    async def _cleanup_client("):]
    cleanup = cleanup.split("\n    async def ", 1)[0]
    stop = transport_src[transport_src.index("    async def stop("):transport_src.index("    def _enqueue_frame")]
    no_binary_clear = "_companion_binary_tags.clear" not in cleanup + stop
    no_discovery_clear = "_companion_discovery_tags.clear" not in cleanup + stop

    control_src = (core_root / "src/openhop_core/node/handlers/control.py").read_text()
    no_callback_expiry = "call_later" not in control_src and "wait_for" not in control_src
    assert no_binary_clear and no_discovery_clear and no_callback_expiry
    return no_binary_clear, no_discovery_clear, no_callback_expiry


def check_default_idle_disconnect() -> int:
    default = inspect.signature(CompanionFrameServer.__init__).parameters[
        "client_idle_timeout_sec"
    ].default
    assert default == 8 * 60 * 60
    return default


async def main() -> None:
    core_root = Path(os.environ.get("OPENHOP_CORE_ROOT", Path(openhop_core.__file__).resolve().parents[2]))
    print("BUG-125 heartbeat frame:", await check_unsolicited_heartbeat())
    print("BUG-126 payloadless packet:", check_payloadless_packet())
    totals, encoded = await check_packet_stats_key_mismatch()
    print("BUG-127 collector totals:", totals)
    print("BUG-127 encoded packet stats:", encoded)
    print("BUG-128 callback counts before/after:", check_callback_erasure())
    print("BUG-129 owner state has no disconnect/timeout cleanup:", check_unexpired_owner_state(core_root))
    print("BUG-130 default idle disconnect seconds:", check_default_idle_disconnect())
    print("All 6 focused checks passed.")


if __name__ == "__main__":
    asyncio.run(main())
