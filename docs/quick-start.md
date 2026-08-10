# Quick Start

This guide verifies that an AAW Lab sEMG module output can be read by a microcontroller ADC and shown in Teleplot.

## What You Need

- AAW Lab sEMG module.
- Arduino-compatible board or ESP32 development board.
- USB cable.
- Battery or another safe isolated supply for the sEMG module.
- Electrodes and electrode leads.
- Teleplot installed on your computer.

## Basic Wiring

| sEMG module | Microcontroller |
| --- | --- |
| `OUT` | ADC input pin |
| `GND` | `GND` |
| `VCC` | Module supply voltage |

If the module exposes `REF` or `VREF`, leave it unconnected for these beginner examples unless the product documentation says otherwise.

## First Test

1. Start with wet electrodes if available.
2. Place electrodes on the forearm muscle you want to observe.
3. Power the sEMG module from a safe isolated supply.
4. Upload one example sketch.
5. Open Teleplot and connect to the board serial port.
6. Relax your hand for a few seconds.
7. Make a fist and release it several times.

## What Success Looks Like

You should see a waveform that changes when the target muscle contracts.

It does not need to look clean during the first test. The first goal is only to confirm that the output reacts to muscle activity.

## Common Problems

| Symptom | Check |
| --- | --- |
| Flat line | Wiring, power, ADC pin, electrode contact |
| Saturated high or low | ADC range, module output range, electrode connection |
| Very noisy waveform | Electrode contact, nearby computer/charger, loose ground, long wires |
| Changes when touching wires | Poor shielding, loose contact, high electrode impedance |

See [`troubleshooting.md`](troubleshooting.md) for more checks.
