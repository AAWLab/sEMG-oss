# AAW sEMG OSS

Beginner-friendly open-source examples and Python tools for reading AAW Lab surface EMG module output.

This repository is for education, research prototyping, electronics development, and non-diagnostic experiments. It is not a medical device project.

## What Is Included

- Basic Arduino analog-read example for Teleplot.
- Basic ESP32 analog-read example for Teleplot.
- Python SDK and CLI for AAW Lab sEMG wireless dongle streams.
- Wiring, electrode placement, and safety notes.
- A simple text output format that is easy to inspect and modify.

## Examples

| Example | Board | Output | Best for |
| --- | --- | --- | --- |
| [`arduino-analog-teleplot`](examples/arduino-analog-teleplot/) | Arduino Uno/Nano/Mega compatible boards | `>emg:512` | First analog-output test |
| [`esp32-analog-teleplot`](examples/esp32-analog-teleplot/) | ESP32 development boards | `>emg:2048` and `>emg_v:1.650` | Quick ESP32 validation |

## Python SDK

The Python SDK lives in [`python/`](python/):

```python
from aawlab_emg import WirelessReader

with WirelessReader("/dev/tty.usbmodemXXX") as reader:
    for event in reader:
        if event.type == "batch":
            print(event.device_id, event.sample_rate_hz, event.samples)
```

CLI examples:

```bash
aaw-emg list
aaw-emg stream --port /dev/tty.usbmodemXXX
aaw-emg record --port /dev/tty.usbmodemXXX --duration 30 --csv trial.csv
```

See [`docs/python-sdk.md`](docs/python-sdk.md).

## Quick Start

1. Connect the sEMG module output to an ADC-capable pin.
2. Power the module from a safe isolated supply. Battery power is recommended for first tests.
3. Upload one of the example sketches.
4. Open Teleplot and connect to the board serial port.
5. Relax your hand, then make a fist. The waveform should change with muscle contraction.

Read [`docs/quick-start.md`](docs/quick-start.md) before testing.

## Teleplot Format

The examples print one sample per line:

```text
>emg:512
```

ESP32 example also prints an estimated voltage:

```text
>emg_v:1.650
```

See [`docs/teleplot.md`](docs/teleplot.md).

## Safety

AAW Lab sEMG modules and examples are for education, research prototyping, electronics development, and non-diagnostic experiments only.

Do not use them for medical diagnosis, treatment, vital-sign monitoring, or safety-critical control. Do not connect human-connected experiments to mains-referenced equipment.

Read [`docs/safety.md`](docs/safety.md).

## License

Code examples are released under the MIT License. Documentation is released under CC BY-NC-SA 4.0. See [`LICENSE`](LICENSE).
