# Arduino Analog Teleplot Example

This example reads an AAW Lab sEMG module analog output with an Arduino ADC pin and prints Teleplot-compatible serial data.

## Wiring

| sEMG module | Arduino |
| --- | --- |
| `OUT` | `A0` |
| `GND` | `GND` |
| `VCC` | Module supply voltage |

Use a safe isolated supply for human-connected tests. Battery power is recommended.

## Serial Output

```text
>emg:512
```

Open Teleplot at `115200` baud and select the Arduino serial port.

## Notes

- This is a minimal validation example.
- It does not implement precision timing, filtering, or recording.
- Start with wet electrodes if this is your first EMG test.
