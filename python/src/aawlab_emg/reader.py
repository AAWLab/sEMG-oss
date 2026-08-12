from __future__ import annotations

import time
from typing import Iterator, Union

import serial

from .events import BatteryEvent, BatchEvent, StatusEvent
from .packets import PacketParser

Event = Union[BatchEvent, BatteryEvent, StatusEvent]


class WirelessReader:
    """Read AAW Lab sEMG wireless dongle events from a USB serial port."""

    def __init__(self, port: str, baudrate: int = 921600, timeout: float = 0.1) -> None:
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.parser = PacketParser()
        self._serial: serial.Serial | None = None
        self._pending: list[Event] = []

    def __enter__(self) -> "WirelessReader":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        self.close()

    def __iter__(self) -> Iterator[Event]:
        if self._serial is None:
            self.open()
        return self

    def __next__(self) -> Event:
        event = self.read_event()
        if event is None:
            raise StopIteration
        return event

    def read_event(self, timeout_s: float | None = None) -> Event | None:
        """Read one event.

        If `timeout_s` is `None`, wait indefinitely. Otherwise return `None`
        when no complete event is available before the timeout.
        """
        if self._pending:
            return self._pending.pop(0)
        if self._serial is None:
            self.open()
        assert self._serial is not None
        deadline = None if timeout_s is None else time.monotonic() + timeout_s
        while True:
            if deadline is not None and time.monotonic() >= deadline:
                return None
            data = self._serial.read(4096)
            if data:
                self._pending.extend(self.parser.feed(data))
                if self._pending:
                    return self._pending.pop(0)
            else:
                time.sleep(0.001)

    def open(self) -> None:
        if self._serial is not None:
            return
        self._serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        self._serial.reset_input_buffer()

    def close(self) -> None:
        if self._serial is not None:
            self._serial.close()
            self._serial = None

    def command(self, command: str) -> None:
        if self._serial is None:
            self.open()
        assert self._serial is not None
        line = command.strip().encode("ascii") + b"\n"
        self._serial.write(line)
        self._serial.flush()

    def pair(self) -> None:
        self.command("pair")

    def clear(self) -> None:
        self.command("clear")

    def request_status(self) -> None:
        self.command("status")
