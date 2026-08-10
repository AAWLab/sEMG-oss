# Teleplot

Teleplot is a simple serial plotting tool. The examples in this repository print Teleplot-compatible lines.

## Basic Format

Each line starts with `>` and uses `name:value`:

```text
>emg:512
```

Teleplot creates a waveform named `emg`.

## ESP32 Voltage Output

The ESP32 example also prints an estimated voltage:

```text
>emg_v:1.650
```

This value is only a quick estimate. ESP32 internal ADC behavior varies by chip, board, attenuation, and calibration.

## Serial Settings

The examples use:

```text
115200 baud
```

If Teleplot shows no data, confirm that the selected serial port and baud rate match the sketch.

## What To Look For

- Relaxed muscle: lower activity.
- Contracted muscle: higher activity or changed waveform shape.
- Constant high or low value: possible saturation or wiring problem.
- Large 50/60 Hz sine-like waveform: likely power-line pickup or poor electrode contact.
