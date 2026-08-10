# ESP32 Analog Teleplot Example

This example reads an AAW Lab sEMG module analog output with an ESP32 ADC pin and prints Teleplot-compatible serial data.

## Default Pin

The sketch uses `GPIO34` by default because it is an input-only ADC pin on many classic ESP32 boards.

If your ESP32 board does not expose `GPIO34`, change `EMG_PIN` in the sketch to a valid ADC pin for your board.

For ESP32-S3 boards, choose an ADC-capable pin exposed by your board and update the sketch.

## Wiring

| sEMG module | ESP32 |
| --- | --- |
| `OUT` | `GPIO34` or another ADC pin |
| `GND` | `GND` |
| `VCC` | Module supply voltage |

Use a safe isolated supply for human-connected tests. Battery power is recommended.

## Serial Output

```text
>emg:2048
>emg_v:1.650
```

Open Teleplot at `115200` baud and select the ESP32 serial port.

## Notes

- ESP32 internal ADC is convenient but not precision instrumentation.
- Use an external ADC for more stable and repeatable EMG acquisition.
- This example is only for quick validation.
