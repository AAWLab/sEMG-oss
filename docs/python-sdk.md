# Python SDK

`aawlab-emg` is a Python SDK and command-line tool for reading AAW Lab sEMG wireless dongle data.

This SDK is for education, research prototyping, electronics development, and non-diagnostic experiments. It is not a medical device tool.

## Install Locally

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Python Example

```python
from aawlab_emg import WirelessReader

with WirelessReader("/dev/tty.usbmodemXXX") as reader:
    for event in reader:
        if event.type == "batch":
            print(event.device_id, event.sample_rate_hz, event.samples)
```

On Windows, the port may look like `COM5`.

## CLI Examples

List serial ports:

```bash
aaw-emg list
```

Print events:

```bash
aaw-emg stream --port /dev/tty.usbmodemXXX
```

Record 30 seconds to CSV:

```bash
aaw-emg record --port /dev/tty.usbmodemXXX --duration 30 --csv trial.csv
```

Record JSON Lines:

```bash
aaw-emg record --port /dev/tty.usbmodemXXX --duration 30 --jsonl trial.jsonl
```

Send dongle commands:

```bash
aaw-emg status --port /dev/tty.usbmodemXXX
aaw-emg pair --port /dev/tty.usbmodemXXX
aaw-emg clear --port /dev/tty.usbmodemXXX
```

## Events

The reader yields three event types:

- `BatchEvent`: raw EMG sample batches from one wireless node.
- `BatteryEvent`: battery telemetry from one wireless node.
- `StatusEvent`: text status printed by the dongle.

For research workflows, keep the raw `int16` values and apply filtering, rectification, envelope extraction, calibration, and feature extraction during analysis.
