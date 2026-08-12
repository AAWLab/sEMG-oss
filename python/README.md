# aawlab-emg Python SDK

Python SDK and command-line tools for reading AAW Lab sEMG wireless dongle streams.

This package is for education, research prototyping, electronics development, and non-diagnostic experiments. It is not for medical diagnosis, treatment, vital-sign monitoring, or safety-critical control.

## Install For Local Development

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
cd python
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -e ".[dev]"
```

## Python API

```python
from aawlab_emg import WirelessReader

with WirelessReader("/dev/tty.usbmodemXXX") as reader:
    for event in reader:
        if event.type == "batch":
            print(event.device_id, event.sample_rate_hz, event.samples)
```

`event.samples` is a NumPy `int16` array.

## CLI

List serial ports:

```bash
aaw-emg list
```

Print incoming events:

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
aaw-emg pair --port /dev/tty.usbmodemXXX
aaw-emg status --port /dev/tty.usbmodemXXX
aaw-emg clear --port /dev/tty.usbmodemXXX
```

## Data Model

The reader yields:

- `BatchEvent`: a batch of raw EMG samples from one device.
- `BatteryEvent`: battery state from one wireless node.
- `StatusEvent`: text status printed by the dongle.

CSV recordings include raw sample values and sample indexes. Keep raw values for research workflows; apply filtering, rectification, envelope extraction, and calibration during analysis.
