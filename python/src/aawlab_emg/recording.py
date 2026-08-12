from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import TextIO

from .events import BatteryEvent, BatchEvent, StatusEvent


class CsvRecorder:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._file: TextIO | None = None
        self._writer: csv.DictWriter[str] | None = None

    def __enter__(self) -> "CsvRecorder":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        self.close()

    def open(self) -> None:
        if self._file is not None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self.path.open("w", newline="", encoding="utf-8")
        self._writer = csv.DictWriter(
            self._file,
            fieldnames=[
                "time_s",
                "host_time_s",
                "device_id",
                "sample_index",
                "sequence",
                "raw",
                "lost_packets",
            ],
        )
        self._writer.writeheader()

    def close(self) -> None:
        if self._file is not None:
            self._file.close()
        self._file = None
        self._writer = None

    def write(self, event: BatchEvent) -> None:
        if self._writer is None:
            self.open()
        assert self._writer is not None
        for offset, raw in enumerate(event.samples.tolist()):
            sample_index = event.first_sample_index + offset
            self._writer.writerow(
                {
                    "time_s": sample_index / event.sample_rate_hz,
                    "host_time_s": event.timestamp_host_s,
                    "device_id": event.device_id,
                    "sample_index": sample_index,
                    "sequence": event.sequence,
                    "raw": raw,
                    "lost_packets": event.lost_packets,
                }
            )


class JsonlRecorder:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._file: TextIO | None = None

    def __enter__(self) -> "JsonlRecorder":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        self.close()

    def open(self) -> None:
        if self._file is not None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self.path.open("w", encoding="utf-8")

    def close(self) -> None:
        if self._file is not None:
            self._file.close()
        self._file = None

    def write(self, event: BatchEvent | BatteryEvent | StatusEvent) -> None:
        if self._file is None:
            self.open()
        assert self._file is not None
        row = asdict(event)
        if isinstance(event, BatchEvent):
            row["samples"] = event.samples.tolist()
        self._file.write(json.dumps(row, separators=(",", ":")) + "\n")
