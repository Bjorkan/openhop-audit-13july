# File-by-file review matrix

This matrix records every source file in the three audit inventories. It was rechecked against Core `41b6201` and Repeater `dd6dfce` after reviewing all 19 commits in the supplied base-to-head ranges. “No additional deviation” means the file was read in context and did not independently establish a new unintentional MeshCore compatibility difference beyond any linked finding. Hardware/UI reference files were reviewed for protocol constants, callbacks, frame layouts and behavior relevant to OpenHop; platform rendering details are intentionally out of scope.

## Core

| File | Review result | Related findings |
|---|---|---|
| `src/openhop_core/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/base_callbacks.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-099](../findings/BUG-099-path-discovery-pushes-replace-encoded-path-lengths-with-raw-byte-counts.md) |
| `src/openhop_core/companion/base_config.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-054](../findings/BUG-054-unsupported-radio-changes-report-success-for-virtual-companions.md), [BUG-078](../findings/BUG-078-companion-node-names-are-limited-by-characters-instead-of-the-31-byte-field.md), [BUG-081](../findings/BUG-081-cmd-set-radio-params-cannot-enable-client-repeat-and-accepts-out-of-range-frequencies.md), [BUG-082](../findings/BUG-082-cmd-set-radio-tx-power-ignores-the-advertised-hardware-limit.md) |
| `src/openhop_core/companion/base_contacts.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/base_events.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/base_send.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-085](../findings/BUG-085-cmd-send-raw-packet-discards-the-requested-transmit-priority.md) |
| `src/openhop_core/companion/base_support.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/binary_parsing.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/channel_store.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/companion_base.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/companion_bridge.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/companion_radio.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/radio_capabilities.py` | Reviewed; centralizes backend maximum-TX-power discovery. It improves BUG-082 but does not enforce the limit in the command handler. | [BUG-082](../findings/BUG-082-cmd-set-radio-tx-power-ignores-the-advertised-hardware-limit.md) |
| `src/openhop_core/companion/constants.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-069](../findings/BUG-069-has-connection-and-get-tuning-params-are-advertised-but-unimplemented.md), [BUG-098](../findings/BUG-098-protocol-level-13-is-reported-while-reboot-device-pin-and-factory-reset-commands-are-absent.md) |
| `src/openhop_core/companion/contact_store.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/frame_server/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/frame_server/commands_channels.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-084](../findings/BUG-084-index-less-cmd-get-channel-emits-a-multi-frame-dump-absent-from-meshcore.md), [BUG-089](../findings/BUG-089-cmd-set-channel-accepts-secret-encodings-that-meshcore-explicitly-rejects.md) |
| `src/openhop_core/companion/frame_server/commands_contacts.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/frame_server/commands_device.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-073](../findings/BUG-073-self-info-omits-the-configured-environment-telemetry-bits.md), [BUG-078](../findings/BUG-078-companion-node-names-are-limited-by-characters-instead-of-the-31-byte-field.md), [BUG-081](../findings/BUG-081-cmd-set-radio-params-cannot-enable-client-repeat-and-accepts-out-of-range-frequencies.md), [BUG-082](../findings/BUG-082-cmd-set-radio-tx-power-ignores-the-advertised-hardware-limit.md), [BUG-087](../findings/BUG-087-short-companion-commands-are-accepted-and-can-silently-mutate-device-state.md), [BUG-090](../findings/BUG-090-cmd-get-custom-vars-applies-its-140-byte-limit-before-utf-8-encoding.md) |
| `src/openhop_core/companion/frame_server/commands_messaging.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-074](../findings/BUG-074-cmd-send-txt-msg-accepts-reserved-text-type-values.md), [BUG-083](../findings/BUG-083-cmd-send-telemetry-req-rejects-meshcore-s-self-telemetry-form.md), [BUG-085](../findings/BUG-085-cmd-send-raw-packet-discards-the-requested-transmit-priority.md), [BUG-086](../findings/BUG-086-cmd-send-trace-path-miscomputes-multi-byte-route-completion-and-timeout-hints.md), [BUG-094](../findings/BUG-094-companion-text-commands-rewrite-invalid-utf-8-payload-bytes.md), [BUG-095](../findings/BUG-095-cmd-send-txt-msg-accepts-a-direct-message-with-no-text-byte.md), [BUG-096](../findings/BUG-096-cmd-send-control-data-rejects-meshcore-s-minimum-one-byte-control-payload.md), [BUG-097](../findings/BUG-097-cmd-send-raw-data-rejects-the-valid-zero-hop-four-byte-minimum-payload.md) |
| `src/openhop_core/companion/frame_server/frames.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/frame_server/push.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-099](../findings/BUG-099-path-discovery-pushes-replace-encoded-path-lengths-with-raw-byte-counts.md) |
| `src/openhop_core/companion/frame_server/server.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-069](../findings/BUG-069-has-connection-and-get-tuning-params-are-advertised-but-unimplemented.md), [BUG-098](../findings/BUG-098-protocol-level-13-is-reported-while-reboot-device-pin-and-factory-reset-commands-are-absent.md) |
| `src/openhop_core/companion/frame_server/transport.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/message_queue.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/models.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-081](../findings/BUG-081-cmd-set-radio-params-cannot-enable-client-repeat-and-accepts-out-of-range-frequencies.md) |
| `src/openhop_core/companion/path_cache.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/stats_collector.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/companion/timing.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/base.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/ch341/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/ch341/ch341_async.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/ch341/ch341_gpio_manager.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/gpio_manager.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/kiss_modem_wrapper.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-088](../findings/BUG-088-kiss-signal-report-negotiation-can-stall-all-received-packet-delivery.md) |
| `src/openhop_core/hardware/kiss_serial_wrapper.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/lora/LoRaRF/SX126x.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/lora/LoRaRF/SX127x.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/lora/LoRaRF/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/lora/LoRaRF/base.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/protocol_constants.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/signal_utils.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/sx1262_wrapper.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/tcp_radio.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/transports/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/transports/ch341_spi_transport.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/transports/spi_transport.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/transports/spidev_transport.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/usb_radio.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/hardware/wsradio.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/dispatcher.py` | Reviewed; contains code relevant to active findings and the now-fixed reception-delay report. | [BUG-066](../findings/BUG-066-the-generic-own-packet-filter-drops-valid-packets-on-one-byte-collisions.md), [BUG-068](../findings/BUG-068-timed-out-dispatcher-ack-waiters-are-never-removed.md), [BUG-072](../findings/BUG-072-malformed-frame-blacklist-storage-is-permanent-and-unbounded.md), [BUG-075](../findings/BUG-075-outbound-packets-are-not-recorded-in-the-dispatcher-seen-table.md), [BUG-076](../findings/BUG-076-concurrent-receive-tasks-race-replay-state-and-reorder-protocol-handling.md), [BUG-077](../findings/BUG-077-standalone-core-lacks-meshcore-s-rolling-transmit-airtime-budget.md), [BUG-023](../archive/findings/BUG-023-flood-packets-bypass-meshcore-s-reception-quality-delay.md) |
| `src/openhop_core/node/events/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/events/event_service.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/events/events.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/ack.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/advert.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/anon_request.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/base.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/control.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/crypto_helpers.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/group_text.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/login_response.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/login_server.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/multipart.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/path.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/protocol_request.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-076](../findings/BUG-076-concurrent-receive-tasks-race-replay-state-and-reorder-protocol-handling.md), [BUG-093](../findings/BUG-093-the-repeater-does-not-implement-meshcore-telemetry-req-responses.md) |
| `src/openhop_core/node/handlers/protocol_response.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-099](../findings/BUG-099-path-discovery-pushes-replace-encoded-path-lengths-with-raw-byte-counts.md) |
| `src/openhop_core/node/handlers/registry.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/result.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/text.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/handlers/trace.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/node/node.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/protocol/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/protocol/constants.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-064](../findings/BUG-064-the-exported-cipher-mac-size-is-32-bytes-instead-of-2.md), [BUG-065](../findings/BUG-065-reserved-payload-version-1-is-accepted-as-a-supported-wire-format.md) |
| `src/openhop_core/protocol/crypto.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/protocol/identity.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-070](../findings/BUG-070-identity-addresses-hash-the-public-key-instead-of-using-its-prefix.md) |
| `src/openhop_core/protocol/modem_identity.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-070](../findings/BUG-070-identity-addresses-hash-the-public-key-instead-of-using-its-prefix.md) |
| `src/openhop_core/protocol/packet.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-002](../archive/findings/BUG-002-packet-payload-limit-is-larger-than-meshcore-s-wire-limit.md), [BUG-065](../findings/BUG-065-reserved-payload-version-1-is-accepted-as-a-supported-wire-format.md) |
| `src/openhop_core/protocol/packet_builder.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-002](../archive/findings/BUG-002-packet-payload-limit-is-larger-than-meshcore-s-wire-limit.md), [BUG-067](../findings/BUG-067-advert-timestamps-share-the-global-unique-request-clock-and-can-run-into-the-future.md) |
| `src/openhop_core/protocol/packet_filter.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-072](../findings/BUG-072-malformed-frame-blacklist-storage-is-permanent-and-unbounded.md) |
| `src/openhop_core/protocol/packet_utils.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-048](../archive/findings/BUG-048-lora-airtime-calculations-use-incompatible-coding-rate-representations.md) |
| `src/openhop_core/protocol/region_map.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/protocol/transport_keys.py` | Reviewed; no additional unintentional deviation identified. | — |
| `src/openhop_core/protocol/utils.py` | Reviewed; no additional unintentional deviation identified. | — |

## Repeater

| File | Review result | Related findings |
|---|---|---|
| `repeater/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/airtime.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-048](../archive/findings/BUG-048-lora-airtime-calculations-use-incompatible-coding-rate-representations.md) |
| `repeater/companion/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/companion/bridge.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-054](../findings/BUG-054-unsupported-radio-changes-report-success-for-virtual-companions.md) |
| `repeater/companion/constants.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/companion/frame_server.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-060](../archive/findings/BUG-060-the-sqlite-queue-loses-binary-payload-signed-sender-and-signal-metadata.md) |
| `repeater/companion/identity_resolve.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/companion/utils.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/config.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/config_manager.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/data_acquisition/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/data_acquisition/glass_handler.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/data_acquisition/gps_service.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/data_acquisition/hardware_stats.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/data_acquisition/mqtt_handler.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/data_acquisition/rrdtool_handler.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/data_acquisition/sqlite_handler.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-060](../archive/findings/BUG-060-the-sqlite-queue-loses-binary-payload-signed-sender-and-signal-metadata.md), [BUG-092](../findings/BUG-092-posting-to-a-room-can-skip-older-unsynced-messages-for-the-author.md) |
| `repeater/data_acquisition/storage_collector.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/data_acquisition/storage_utils.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/data_acquisition/websocket_handler.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/engine.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/handler_helpers/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/handler_helpers/acl.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/handler_helpers/advert.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/handler_helpers/discovery.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/handler_helpers/login.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/handler_helpers/mesh_cli.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-079](../findings/BUG-079-exposed-repeater-cli-maintenance-commands-remain-no-op-stubs.md) |
| `repeater/handler_helpers/path.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/handler_helpers/protocol_request.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-071](../findings/BUG-071-repeater-status-hardcodes-tx-queue-depth-and-error-events-to-zero.md), [BUG-093](../findings/BUG-093-the-repeater-does-not-implement-meshcore-telemetry-req-responses.md) |
| `repeater/handler_helpers/room_server.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-080](../findings/BUG-080-room-server-post-length-uses-160-characters-instead-of-151-wire-bytes.md), [BUG-091](../findings/BUG-091-room-server-pushes-replace-the-post-timestamp-and-omit-retry-attempt-entropy.md), [BUG-092](../findings/BUG-092-posting-to-a-room-can-skip-older-unsynced-messages-for-the-author.md), [BUG-100](../findings/BUG-100-the-global-room-server-rate-limiter-releases-its-lock-before-transmission-begins.md) |
| `repeater/handler_helpers/text.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/handler_helpers/trace.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/identity_manager.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/keygen.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/local_cli.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/main.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/neighbour_links.py` | Reviewed; bounded, monotonic-time observational neighbour metrics only. It does not alter forwarding, deduplication, route selection or packet acceptance. | — |
| `repeater/packet_router.py` | Reviewed; contains code relevant to one or more active findings. | [BUG-022](../findings/BUG-022-multipart-packets-and-routed-acks-lack-their-special-forwarding-paths.md) |
| `repeater/policy_engine.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/presets/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/base.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/ens210.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/hardware_stats.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/ina219.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/lafvin_ups_3s.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/manager.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/pymc_modem.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/registry.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/shtc3.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/waveshare_ups_d.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/sensors/waveshare_ups_e.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/service_utils.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/utils_packet.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/api_endpoints.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/auth/__init__.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/auth/api_tokens.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/auth/cherrypy_tool.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/auth/jwt_handler.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/auth/middleware.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/auth_endpoints.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/cad_calibration_engine.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/companion_endpoints.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/companion_ws_proxy.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/http_server.py` | Reviewed; no additional unintentional deviation identified. | — |
| `repeater/web/update_endpoints.py` | Reviewed; no additional unintentional deviation identified. | — |

## MeshCore

| File | Review result | Related findings |
|---|---|---|
| `examples/companion_radio/AbstractUITask.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/DataStore.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/DataStore.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/MyMesh.cpp` | Reviewed; contains code relevant to one or more active findings. | [BUG-069](../findings/BUG-069-has-connection-and-get-tuning-params-are-advertised-but-unimplemented.md), [BUG-073](../findings/BUG-073-self-info-omits-the-configured-environment-telemetry-bits.md), [BUG-074](../findings/BUG-074-cmd-send-txt-msg-accepts-reserved-text-type-values.md), [BUG-078](../findings/BUG-078-companion-node-names-are-limited-by-characters-instead-of-the-31-byte-field.md), [BUG-081](../findings/BUG-081-cmd-set-radio-params-cannot-enable-client-repeat-and-accepts-out-of-range-frequencies.md), [BUG-082](../findings/BUG-082-cmd-set-radio-tx-power-ignores-the-advertised-hardware-limit.md), [BUG-083](../findings/BUG-083-cmd-send-telemetry-req-rejects-meshcore-s-self-telemetry-form.md), [BUG-084](../findings/BUG-084-index-less-cmd-get-channel-emits-a-multi-frame-dump-absent-from-meshcore.md), [BUG-085](../findings/BUG-085-cmd-send-raw-packet-discards-the-requested-transmit-priority.md), [BUG-086](../findings/BUG-086-cmd-send-trace-path-miscomputes-multi-byte-route-completion-and-timeout-hints.md), [BUG-087](../findings/BUG-087-short-companion-commands-are-accepted-and-can-silently-mutate-device-state.md), [BUG-089](../findings/BUG-089-cmd-set-channel-accepts-secret-encodings-that-meshcore-explicitly-rejects.md), [BUG-090](../findings/BUG-090-cmd-get-custom-vars-applies-its-140-byte-limit-before-utf-8-encoding.md), [BUG-094](../findings/BUG-094-companion-text-commands-rewrite-invalid-utf-8-payload-bytes.md), [BUG-095](../findings/BUG-095-cmd-send-txt-msg-accepts-a-direct-message-with-no-text-byte.md), [BUG-096](../findings/BUG-096-cmd-send-control-data-rejects-meshcore-s-minimum-one-byte-control-payload.md), [BUG-097](../findings/BUG-097-cmd-send-raw-data-rejects-the-valid-zero-hop-four-byte-minimum-payload.md), [BUG-098](../findings/BUG-098-protocol-level-13-is-reported-while-reboot-device-pin-and-factory-reset-commands-are-absent.md), [BUG-099](../findings/BUG-099-path-discovery-pushes-replace-encoded-path-lengths-with-raw-byte-counts.md) |
| `examples/companion_radio/MyMesh.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/NodePrefs.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/main.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-new/UITask.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-new/UITask.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-new/icons.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-orig/Button.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-orig/Button.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-orig/UITask.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-orig/UITask.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-tiny/ScrollingStatusBar.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-tiny/UITask.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-tiny/UITask.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/companion_radio/ui-tiny/u8g2_icons.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/kiss_modem/KissModem.cpp` | Reviewed; contains code relevant to one or more active findings. | [BUG-088](../findings/BUG-088-kiss-signal-report-negotiation-can-stall-all-received-packet-delivery.md) |
| `examples/kiss_modem/KissModem.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/kiss_modem/main.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_repeater/MyMesh.cpp` | Reviewed; contains code relevant to one or more active findings. | [BUG-071](../findings/BUG-071-repeater-status-hardcodes-tx-queue-depth-and-error-events-to-zero.md), [BUG-093](../findings/BUG-093-the-repeater-does-not-implement-meshcore-telemetry-req-responses.md) |
| `examples/simple_repeater/MyMesh.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_repeater/RateLimiter.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_repeater/UITask.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_repeater/UITask.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_repeater/main.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_room_server/MyMesh.cpp` | Reviewed; contains code relevant to one or more active findings. | [BUG-080](../findings/BUG-080-room-server-post-length-uses-160-characters-instead-of-151-wire-bytes.md), [BUG-091](../findings/BUG-091-room-server-pushes-replace-the-post-timestamp-and-omit-retry-attempt-entropy.md), [BUG-092](../findings/BUG-092-posting-to-a-room-can-skip-older-unsynced-messages-for-the-author.md), [BUG-100](../findings/BUG-100-the-global-room-server-rate-limiter-releases-its-lock-before-transmission-begins.md) |
| `examples/simple_room_server/MyMesh.h` | Official reference establishing one or more compatibility findings. | [BUG-080](../findings/BUG-080-room-server-post-length-uses-160-characters-instead-of-151-wire-bytes.md) |
| `examples/simple_room_server/UITask.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_room_server/UITask.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_room_server/main.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_secure_chat/main.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_sensor/SensorMesh.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_sensor/SensorMesh.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_sensor/TimeSeriesData.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_sensor/TimeSeriesData.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_sensor/UITask.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_sensor/UITask.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `examples/simple_sensor/main.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/Dispatcher.cpp` | Official reference establishing one or more compatibility findings. | [BUG-065](../findings/BUG-065-reserved-payload-version-1-is-accepted-as-a-supported-wire-format.md), [BUG-076](../findings/BUG-076-concurrent-receive-tasks-race-replay-state-and-reorder-protocol-handling.md), [BUG-077](../findings/BUG-077-standalone-core-lacks-meshcore-s-rolling-transmit-airtime-budget.md) |
| `src/Dispatcher.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/Identity.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/Identity.h` | Official reference establishing one or more compatibility findings. | [BUG-070](../findings/BUG-070-identity-addresses-hash-the-public-key-instead-of-using-its-prefix.md) |
| `src/Mesh.cpp` | Reviewed; contains code relevant to one or more active findings. | [BUG-066](../findings/BUG-066-the-generic-own-packet-filter-drops-valid-packets-on-one-byte-collisions.md), [BUG-067](../findings/BUG-067-advert-timestamps-share-the-global-unique-request-clock-and-can-run-into-the-future.md), [BUG-075](../findings/BUG-075-outbound-packets-are-not-recorded-in-the-dispatcher-seen-table.md), [BUG-086](../findings/BUG-086-cmd-send-trace-path-miscomputes-multi-byte-route-completion-and-timeout-hints.md) |
| `src/Mesh.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/MeshCore.h` | Official reference establishing one or more compatibility findings. | [BUG-064](../findings/BUG-064-the-exported-cipher-mac-size-is-32-bytes-instead-of-2.md) |
| `src/Packet.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/Packet.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/Utils.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/Utils.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/AbstractBridge.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/AdvertDataHelpers.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/AdvertDataHelpers.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ArduinoHelpers.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ArduinoSerialInterface.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ArduinoSerialInterface.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/AutoDiscoverRTCClock.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/AutoDiscoverRTCClock.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/BaseChatMesh.cpp` | Reviewed; contains code relevant to one or more active findings. | [BUG-094](../findings/BUG-094-companion-text-commands-rewrite-invalid-utf-8-payload-bytes.md) |
| `src/helpers/BaseChatMesh.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/BaseSerialInterface.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ChannelDetails.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ClientACL.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ClientACL.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/CommonCLI.cpp` | Official reference establishing one or more compatibility findings. | [BUG-079](../findings/BUG-079-exposed-repeater-cli-maintenance-commands-remain-no-op-stubs.md) |
| `src/helpers/CommonCLI.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ContactInfo.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ESP32Board.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ESP32Board.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/IdentityStore.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/IdentityStore.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/MeshadventurerBoard.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/NRF52Board.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/NRF52Board.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/RTC_RX8130CE.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/RTC_RX8130CE.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/RefCountedDigitalPin.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/RegionMap.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/RegionMap.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/SensorManager.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/SimpleMeshTables.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/StaticPoolPacketManager.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/StaticPoolPacketManager.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/StatsFormatHelper.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/TransportKeyStore.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/TransportKeyStore.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/TxtDataHelpers.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/TxtDataHelpers.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/bridges/BridgeBase.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/bridges/BridgeBase.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/bridges/ESPNowBridge.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/bridges/ESPNowBridge.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/bridges/RS232Bridge.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/bridges/RS232Bridge.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/esp32/ESPNOWRadio.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/esp32/ESPNOWRadio.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/esp32/SerialBLEInterface.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/esp32/SerialBLEInterface.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/esp32/SerialWifiInterface.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/esp32/SerialWifiInterface.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/esp32/TBeamBoard.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/esp32/TBeamBoard.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/nrf52/SerialBLEInterface.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/nrf52/SerialBLEInterface.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomLLCC68.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomLLCC68Wrapper.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomLR1110.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomLR1110Wrapper.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomSTM32WLx.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomSTM32WLxWrapper.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomSX1262.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomSX1262Wrapper.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomSX1268.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomSX1268Wrapper.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomSX1276.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/CustomSX1276Wrapper.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/LR11x0Reset.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/RadioLibWrappers.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/RadioLibWrappers.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/radiolib/SX126xReset.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/sensors/EnvironmentSensorManager.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/sensors/EnvironmentSensorManager.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/sensors/LPPDataHelpers.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/sensors/LocationProvider.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/sensors/MicroNMEALocationProvider.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/sensors/RAK12035_SoilMoisture.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/sensors/RAK12035_SoilMoisture.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/stm32/InternalFileSystem.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/stm32/InternalFileSystem.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/stm32/STM32Board.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/DisplayDriver.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/E213Display.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/E213Display.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/E290Display.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/E290Display.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/GenericVibration.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/GenericVibration.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/GxEPDDisplay.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/GxEPDDisplay.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/LGFXDisplay.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/LGFXDisplay.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/MomentaryButton.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/MomentaryButton.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/NullDisplayDriver.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/OLEDDisplay.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/OLEDDisplay.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/OLEDDisplayFonts.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/OLEDDisplayFonts.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/SH1106Display.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/SH1106Display.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/SSD1306Display.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/SSD1306Display.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/ST7735Display.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/ST7735Display.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/ST7789Display.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/ST7789Display.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/ST7789LCDDisplay.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/ST7789LCDDisplay.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/ST7789Spi.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/U8g2Display.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/UIScreen.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/buzzer.cpp` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |
| `src/helpers/ui/buzzer.h` | Official reference reviewed; no additional OpenHop deviation identified from this file. | — |

## Deeper logic pass addendum

The following cross-file paths received an additional state-machine review. This supplements, rather than replaces, the complete inventory above.

| Project | File | New findings |
|---|---|---|
| Core | `src/openhop_core/node/dispatcher.py` | BUG-101, BUG-105 |
| Core | `src/openhop_core/node/handlers/text.py` | BUG-103, BUG-106, BUG-110, BUG-112, BUG-113, BUG-114, BUG-118 |
| Core | `src/openhop_core/node/handlers/login_server.py` | BUG-107 |
| Core | `src/openhop_core/node/handlers/protocol_request.py` | BUG-115 |
| Core | `src/openhop_core/companion/base_send.py` | BUG-103 |
| Core | `src/openhop_core/companion/companion_bridge.py` | BUG-105 |
| Core | `src/openhop_core/companion/companion_radio.py` | BUG-101, BUG-105 |
| Core | `src/openhop_core/companion/frame_server/commands_contacts.py` | BUG-104 |
| Repeater | `repeater/packet_router.py` | BUG-102 |
| Repeater | `repeater/handler_helpers/acl.py` | BUG-107, BUG-108, BUG-109, BUG-110, BUG-111, BUG-118 |
| Repeater | `repeater/handler_helpers/login.py` | BUG-111 |
| Repeater | `repeater/handler_helpers/text.py` | BUG-109, BUG-110, BUG-113, BUG-114, BUG-116, BUG-117, BUG-118 |
| Repeater | `repeater/handler_helpers/room_server.py` | BUG-110, BUG-114 |
| Repeater | `repeater/handler_helpers/protocol_request.py` | BUG-115 |
| MeshCore | `src/Mesh.cpp` | BUG-101, BUG-102 |
| MeshCore | `src/helpers/BaseChatMesh.cpp` | BUG-103, BUG-105, BUG-106, BUG-112, BUG-115 |
| MeshCore | `src/helpers/ClientACL.h` / `ClientACL.cpp` | BUG-107, BUG-111 |
| MeshCore | `examples/companion_radio/MyMesh.cpp` | BUG-104, BUG-105 |
| MeshCore | `examples/simple_repeater/MyMesh.cpp` | BUG-115, BUG-117, BUG-118 |
| MeshCore | `examples/simple_room_server/MyMesh.cpp` | BUG-108, BUG-109, BUG-110, BUG-113, BUG-114, BUG-116, BUG-117, BUG-118 |

## Continued deep review addendum

| Project | File | New findings |
|---|---|---|
| Core | `src/openhop_core/companion/base_send.py` | BUG-119 |
| Core | `src/openhop_core/node/handlers/login_response.py` | BUG-120 |
| Core | `src/openhop_core/protocol/identity.py` | BUG-121 |
| Core | `src/openhop_core/companion/frame_server/commands_contacts.py` | BUG-123 |
| Core | `src/openhop_core/companion/base_contacts.py` | BUG-123 |
| Core | `src/openhop_core/protocol/packet_utils.py` | BUG-124 |
| Core | `src/openhop_core/hardware/kiss_modem_wrapper.py` | BUG-124 |
| Repeater | `repeater/identity_manager.py` | BUG-121 |
| Repeater | `repeater/engine.py` | BUG-122 |
| MeshCore | `examples/companion_radio/MyMesh.cpp` | BUG-119, BUG-120, BUG-121, BUG-123 |
| MeshCore | `src/helpers/BaseChatMesh.cpp` | BUG-120 |
| MeshCore | `examples/simple_repeater/main.cpp` | BUG-121 |
| MeshCore | `src/Mesh.cpp` | BUG-122 |
| MeshCore | `src/helpers/radiolib/RadioLibWrappers.cpp` | BUG-124 |

## Latest commit and protocol-lifecycle addendum

| Project | File | Review result |
|---|---|---|
| Core | `src/openhop_core/node/dispatcher.py` | Latest flood metric extraction and hash cleanup reviewed; no existing status transition. |
| Core | `src/openhop_core/protocol/packet_utils.py` | Shared flood metrics reviewed; BUG-023 remains fixed and BUG-124 remains open. |
| Core | `src/openhop_core/hardware/sx1262_wrapper.py` | New commits are diagnostics/formatting; no audit regression found. |
| Repeater | `repeater/engine.py` | Shared metrics and neighbour reporting reviewed; no forwarding-policy status transition. |
| Repeater | `repeater/handler_helpers/trace.py` | Route predicate adjustment reviewed; no existing finding changed. |
| Core | `src/openhop_core/companion/frame_server/transport.py` | BUG-125, BUG-129, BUG-130. |
| Core | `src/openhop_core/protocol/packet.py` | BUG-126. |
| Core | `src/openhop_core/companion/stats_collector.py` | BUG-127. |
| Core | `src/openhop_core/companion/frame_server/commands_device.py` | BUG-127. |
| Repeater | `repeater/main.py` | BUG-127. |
| Core | `src/openhop_core/companion/base_callbacks.py` | BUG-128. |
| Core | `src/openhop_core/companion/frame_server/push.py` | BUG-128, BUG-129. |
| Core | `src/openhop_core/companion/frame_server/commands_messaging.py` | BUG-129. |
| Core | `src/openhop_core/companion/frame_server/server.py` | BUG-130. |
| Repeater | `repeater/companion/frame_server.py` | BUG-128, BUG-130. |
| MeshCore | `src/Packet.cpp` | Official reference for BUG-126. |
| MeshCore | `examples/companion_radio/MyMesh.cpp` / `MyMesh.h` | Official references for BUG-125, BUG-127, BUG-129 and BUG-130. |
