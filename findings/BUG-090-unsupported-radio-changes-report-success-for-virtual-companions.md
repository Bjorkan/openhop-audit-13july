# BUG-090 — Unsupported radio changes report success for virtual companions

[← Bug list](../README.md#bug-list)

| Field | Value |
|---|---|
| Severity | **Medium** |
| Area | Companion/repeater integration |
| Affected components | OpenHop Core, OpenHop Repeater |
| Status | Confirmed from the supplied source snapshots |

## TL;DR

A virtual companion can receive success for radio changes that only alter its stored preferences while the shared repeater radio remains unchanged. Core must gate mutations through an explicit capability result, and Repeater must reject shared-radio mutations from virtual companion sessions.

## What happens

### OpenHop Core

The generic command handlers always call preference-mutating setters and then emit OK, even when an integration does not own or permit mutation of the physical radio. Setter return values are also ignored.

### OpenHop Repeater

Repeater-hosted virtual companions inherit preference-only radio setters. Commands can therefore return success and store contradictory per-companion values while the shared physical repeater radio remains unchanged.

## How official MeshCore handles it

### Relevant to OpenHop Core

A successful radio command means the node accepted and applied or persisted the actual radio configuration. Unsupported operations return an error.

### Relevant to OpenHop Repeater

A dedicated companion radio may apply the change, but a virtual identity sharing a repeater radio must not be allowed to reconfigure global RF state through an unaffiliated client session.

## How the OpenHop stack handles it

### OpenHop Core

`_cmd_set_radio_params` and `_cmd_set_tx_power` can report success after changing only NodePrefs or after a hardware setter reports failure.

### OpenHop Repeater

RepeaterCompanionBridge does not override or deny the mutation capability, so the generic core setters change only persisted NodePrefs.

## What needs to change

### OpenHop Core

Introduce explicit capability-gated mutation methods whose result distinguishes applied, rejected/unsupported, and invalid/failed. Command handlers must emit OK only after an applied result and must not pre-mutate preferences. Preserve support for dedicated companion-radio integrations that genuinely own their radio.

### OpenHop Repeater

Implement the repeater side of the core capability API as read-only: reject SET_RADIO_PARAMS and SET_RADIO_TX_POWER with unsupported, do not mutate per-companion preferences, and leave administrative radio changes to a separately authenticated repeater-owned API.

## Source links

These links point to the branches reviewed for this audit. Line numbers can move after later commits.

| Project | Why it matters | Source |
|---|---|---|
| MeshCore | Reference | [`examples/companion_radio/MyMesh.cpp` L1365–L1410](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L1365-L1410) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/base_config.py` L58–L79](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_config.py#L58-L79) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/frame_server/commands_device.py` L279–L309](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/frame_server/commands_device.py#L279-L309) |
| OpenHop Core | Affected implementation | [`src/openhop_core/companion/companion_radio.py` L209–L230](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/companion_radio.py#L209-L230) |
| OpenHop Repeater | Affected implementation | [`repeater/companion/bridge.py` L55–L91](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/companion/bridge.py#L55-L91) |
| OpenHop Repeater | Affected implementation | [`repeater/main.py` L600–L692](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/main.py#L600-L692) |

## Relevant source excerpts

The excerpts are collapsed to keep the report easy to scan.

<details>
<summary><strong>MeshCore</strong> — <code>examples/companion_radio/MyMesh.cpp</code> (L1365–L1410)</summary>

[Open the cited range on GitHub](https://github.com/meshcore-dev/MeshCore/blob/main/examples/companion_radio/MyMesh.cpp#L1365-L1410)

```cpp
1365 |   } else if (cmd_frame[0] == CMD_SET_RADIO_PARAMS) {
1366 |     int i = 1;
1367 |     uint32_t freq;
1368 |     memcpy(&freq, &cmd_frame[i], 4);
1369 |     i += 4;
1370 |     uint32_t bw;
1371 |     memcpy(&bw, &cmd_frame[i], 4);
1372 |     i += 4;
1373 |     uint8_t sf = cmd_frame[i++];
1374 |     uint8_t cr = cmd_frame[i++];
1375 |     uint8_t repeat = 0;  // default - false
1376 |     if (len > i) {
1377 |       repeat = cmd_frame[i++];   // FIRMWARE_VER_CODE  9+
1378 |     }
1379 | 
1380 |     if (repeat && !isValidClientRepeatFreq(freq)) {
1381 |       writeErrFrame(ERR_CODE_ILLEGAL_ARG);
1382 |     } else if (freq >= 150000 && freq <= 2500000 && sf >= 5 && sf <= 12 && cr >= 5 && cr <= 8 && bw >= 7000 &&
1383 |         bw <= 500000) {
1384 |       _prefs.sf = sf;
1385 |       _prefs.cr = cr;
1386 |       _prefs.freq = (float)freq / 1000.0;
1387 |       _prefs.bw = (float)bw / 1000.0;
1388 |       _prefs.client_repeat = repeat;
1389 |       savePrefs();
1390 | 
1391 |       radio_driver.setParams(_prefs.freq, _prefs.bw, _prefs.sf, _prefs.cr);
1392 |       MESH_DEBUG_PRINTLN("OK: CMD_SET_RADIO_PARAMS: f=%d, bw=%d, sf=%d, cr=%d", freq, bw, (uint32_t)sf,
1393 |                          (uint32_t)cr);
1394 | 
1395 |       writeOKFrame();
1396 |     } else {
1397 |       MESH_DEBUG_PRINTLN("Error: CMD_SET_RADIO_PARAMS: f=%d, bw=%d, sf=%d, cr=%d", freq, bw, (uint32_t)sf,
1398 |                          (uint32_t)cr);
1399 |       writeErrFrame(ERR_CODE_ILLEGAL_ARG);
1400 |     }
1401 |   } else if (cmd_frame[0] == CMD_SET_RADIO_TX_POWER) {
1402 |     int8_t power = (int8_t)cmd_frame[1];
1403 |     if (power < -9 || power > MAX_LORA_TX_POWER) {
1404 |       writeErrFrame(ERR_CODE_ILLEGAL_ARG);
1405 |     } else {
1406 |       _prefs.tx_power_dbm = power;
1407 |       savePrefs();
1408 |       radio_driver.setTxPower(_prefs.tx_power_dbm);
1409 |       writeOKFrame();
1410 |     }
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/base_config.py</code> (L58–L79)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/base_config.py#L58-L79)

```python
58 |     def set_radio_params(self, freq_hz: int, bw_hz: int, sf: int, cr: int) -> bool:
59 |         """Set radio parameters (frequency, bandwidth, SF, CR)."""
60 |         if not (5 <= sf <= 12):
61 |             raise ValueError(f"Spreading factor out of range: {sf}")
62 |         if not (5 <= cr <= 8):
63 |             raise ValueError(f"Coding rate out of range: {cr}")
64 |         self.prefs.frequency_hz = freq_hz
65 |         self.prefs.bandwidth_hz = bw_hz
66 |         self.prefs.spreading_factor = sf
67 |         self.prefs.coding_rate = cr
68 |         self._save_prefs()
69 |         return True
70 | 
71 |     def set_tx_power(self, power_dbm: int) -> bool:
72 |         """Set the transmit power in dBm."""
73 |         self.prefs.tx_power_dbm = power_dbm
74 |         self._save_prefs()
75 |         return True
76 | 
77 |     def set_tuning_params(self, rx_delay: float, airtime_factor: float) -> None:
78 |         """Set RX delay and airtime factor tuning parameters."""
79 |         self.prefs.rx_delay_base = rx_delay
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/frame_server/commands_device.py</code> (L279–L309)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/frame_server/commands_device.py#L279-L309)

```python
279 |     async def _cmd_set_radio_params(self, data: bytes) -> None:
280 |         if len(data) < 10:
281 |             self._write_err(ERR_CODE_ILLEGAL_ARG)
282 |             return
283 |         # Frequency in kHz (match firmware self-info; client sends same encoding)
284 |         freq_khz = struct.unpack_from("<I", data, 0)[0]
285 |         bw = struct.unpack_from("<I", data, 4)[0]
286 |         sf = data[8]
287 |         cr = data[9]
288 |         if not (100_000 <= freq_khz <= 2_500_000):
289 |             self._write_err(ERR_CODE_ILLEGAL_ARG)
290 |             return
291 |         if not (7000 <= bw <= 500000):
292 |             self._write_err(ERR_CODE_ILLEGAL_ARG)
293 |             return
294 |         if not (5 <= sf <= 12) or not (5 <= cr <= 8):
295 |             self._write_err(ERR_CODE_ILLEGAL_ARG)
296 |             return
297 |         self.bridge.set_radio_params(freq_khz * 1000, bw, sf, cr)
298 |         self._write_ok()
299 | 
300 |     async def _cmd_set_tx_power(self, data: bytes) -> None:
301 |         if len(data) < 1:
302 |             self._write_err(ERR_CODE_ILLEGAL_ARG)
303 |             return
304 |         power = struct.unpack_from("<b", data, 0)[0]
305 |         if power < -9 or power >= 30:
306 |             self._write_err(ERR_CODE_ILLEGAL_ARG)
307 |             return
308 |         self.bridge.set_tx_power(power)
309 |         self._write_ok()
```

</details>

<details>
<summary><strong>OpenHop Core</strong> — <code>src/openhop_core/companion/companion_radio.py</code> (L209–L230)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_core/blob/dev/src/openhop_core/companion/companion_radio.py#L209-L230)

```python
209 |     def set_radio_params(self, freq_hz: int, bw_hz: int, sf: int, cr: int) -> bool:
210 |         super().set_radio_params(freq_hz, bw_hz, sf, cr)
211 |         if hasattr(self._radio, "configure_radio"):
212 |             try:
213 |                 self._radio.configure_radio(
214 |                     frequency=freq_hz,
215 |                     bandwidth=bw_hz,
216 |                     spreading_factor=sf,
217 |                     coding_rate=cr,
218 |                 )
219 |                 return True
220 |             except Exception as e:
221 |                 logger.error("Error configuring radio: %s", e)
222 |                 return False
223 |         return True
224 | 
225 |     def set_tx_power(self, power_dbm: int) -> bool:
226 |         super().set_tx_power(power_dbm)
227 |         if hasattr(self._radio, "set_tx_power"):
228 |             try:
229 |                 self._radio.set_tx_power(power_dbm)
230 |                 return True
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/companion/bridge.py</code> (L55–L91)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/companion/bridge.py#L55-L91)

```python
55 | 
56 | class RepeaterCompanionBridge(CompanionBridge):
57 |     """CompanionBridge that persists and loads prefs (full NodePrefs) via SQLite JSON blob."""
58 | 
59 |     def __init__(
60 |         self,
61 |         identity,
62 |         packet_injector: Callable[..., Any],
63 |         node_name: str = "pyMC",
64 |         adv_type: int = 1,
65 |         max_contacts: int = 1000,
66 |         max_channels: int = 40,
67 |         offline_queue_size: int = 512,
68 |         radio_config: Optional[dict] = None,
69 |         authenticate_callback: Optional[Callable[..., tuple[bool, int]]] = None,
70 |         initial_contacts: Optional[Any] = None,
71 |         *,
72 |         sqlite_handler=None,
73 |         companion_hash: str = "",
74 |         on_prefs_saved: Optional[Callable[[str], None]] = None,
75 |     ) -> None:
76 |         self._sqlite_handler = sqlite_handler
77 |         self._companion_hash = companion_hash
78 |         self._on_prefs_saved = on_prefs_saved
79 |         super().__init__(
80 |             identity=identity,
81 |             packet_injector=packet_injector,
82 |             node_name=node_name,
83 |             adv_type=adv_type,
84 |             max_contacts=max_contacts,
85 |             max_channels=max_channels,
86 |             offline_queue_size=offline_queue_size,
87 |             radio_config=radio_config,
88 |             authenticate_callback=authenticate_callback,
89 |             initial_contacts=initial_contacts,
90 |         )
91 | 
```

</details>

<details>
<summary><strong>OpenHop Repeater</strong> — <code>repeater/main.py</code> (L600–L608, L669–L685)</summary>

[Open the cited range on GitHub](https://github.com/openhop-dev/openhop_repeater/blob/dev/repeater/main.py#L600-L692)

```python
600 |                 bridge = RepeaterCompanionBridge(
601 |                     identity=identity,
602 |                     # Tag the injector with this companion's hash so inject_packet can
603 |                     # skip its own frame server when echoing TX as raw RX (a node never
604 |                     # hears its own transmission).
605 |                     packet_injector=functools.partial(
606 |                         self.router.inject_packet, origin_hash=companion_hash_str
607 |                     ),
608 |                     node_name=node_name,
…
669 |                             )
670 | 
671 |                 # Ensure public channel (0) exists with default key for new companions
672 |                 from repeater.companion.constants import DEFAULT_PUBLIC_CHANNEL_SECRET
673 | 
674 |                 if bridge.get_channel(0) is None:
675 |                     bridge.set_channel(0, "Public", DEFAULT_PUBLIC_CHANNEL_SECRET)
676 | 
677 |                 self.companion_bridges[companion_hash] = bridge
678 | 
679 |                 frame_server = CompanionFrameServer(
680 |                     bridge=bridge,
681 |                     companion_hash=companion_hash_str,
682 |                     port=tcp_port,
683 |                     bind_address=bind_address,
684 |                     client_idle_timeout_sec=client_idle_timeout_sec,
685 |                     sqlite_handler=sqlite_handler,
```

</details>
