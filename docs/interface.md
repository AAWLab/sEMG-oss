# Interface Notes

AAW Lab sEMG modules provide an analog output that can be connected to an ADC, oscilloscope, Arduino, ESP32, STM32, or other acquisition device.

## Typical Pins

| Pin | Meaning |
| --- | --- |
| `VCC` | Module supply voltage |
| `GND` | Ground reference |
| `OUT` | Analog sEMG output |
| `REF` / `VREF` | Internal output reference, if exposed |
| `IN+`, `IN-`, `REF_ELEC` | Electrode inputs, depending on module variant |

Always check the product-specific documentation before wiring.

## ADC Input

For beginner tests, connect `OUT` to one ADC input and print the ADC value.

For higher-quality acquisition, use an external ADC with a stable sampling rate and suitable input range.

## Sampling Rate

Use at least 800 Hz for a useful EMG waveform. 1000 Hz or higher is recommended for many experiments.

The beginner examples are intentionally simple and do not guarantee precise timing.

## Output Range

The module output is an analog voltage. Make sure the output range does not exceed the ADC input range of your board.

If the waveform is clipped at the top or bottom, check the ADC range and the module gain.
