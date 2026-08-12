from __future__ import annotations

import argparse
import time

from aawlab_emg import WirelessReader
from aawlab_emg.events import BatchEvent
from aawlab_emg.recording import CsvRecorder


def main() -> None:
    parser = argparse.ArgumentParser(description="Save AAW Lab sEMG wireless data to CSV")
    parser.add_argument("--port", required=True)
    parser.add_argument("--csv", required=True)
    parser.add_argument("--duration", type=float, default=30.0)
    args = parser.parse_args()

    started = time.monotonic()
    with WirelessReader(args.port) as reader, CsvRecorder(args.csv) as recorder:
        while time.monotonic() - started < args.duration:
            event = next(reader)
            if isinstance(event, BatchEvent):
                recorder.write(event)


if __name__ == "__main__":
    main()
