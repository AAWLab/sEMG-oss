from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

from .events import BatteryEvent, BatchEvent, StatusEvent
from .reader import WirelessReader
from .recording import CsvRecorder, JsonlRecorder
from .serial_utils import list_serial_ports


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aaw-emg", description="AAW Lab sEMG wireless dongle tools")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="list serial ports")

    stream = sub.add_parser("stream", help="print incoming events")
    add_port_args(stream)
    stream.add_argument("--format", choices=["text", "jsonl"], default="text")

    record = sub.add_parser("record", help="record incoming data")
    add_port_args(record)
    record.add_argument("--duration", type=float, required=True, help="recording duration in seconds")
    record.add_argument("--csv", type=Path, help="CSV output path for batch samples")
    record.add_argument("--jsonl", type=Path, help="JSON Lines output path for all events")

    for name in ["pair", "clear", "status"]:
        cmd = sub.add_parser(name, help=f"send {name} command to dongle")
        add_port_args(cmd)
        cmd.add_argument("--listen", type=float, default=5.0, help="seconds to print responses after command")

    args = parser.parse_args(argv)

    if args.command == "list":
        return cmd_list()
    if args.command == "stream":
        return cmd_stream(args)
    if args.command == "record":
        return cmd_record(args)
    if args.command in {"pair", "clear", "status"}:
        return cmd_send(args.command, args)
    return 2


def add_port_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--port", required=True, help="serial port, for example COM5 or /dev/tty.usbmodemXXX")
    parser.add_argument("--baudrate", type=int, default=921600, help="serial baudrate")


def cmd_list() -> int:
    ports = list_serial_ports()
    if not ports:
        print("No serial ports found.")
        return 0
    for port in ports:
        details = []
        if port.manufacturer:
            details.append(f"manufacturer={port.manufacturer}")
        if port.product:
            details.append(f"product={port.product}")
        if port.serial_number:
            details.append(f"serial={port.serial_number}")
        suffix = " " + " ".join(details) if details else ""
        print(f"{port.device}\t{port.description}{suffix}")
    return 0


def cmd_stream(args: argparse.Namespace) -> int:
    with WirelessReader(args.port, baudrate=args.baudrate) as reader:
        for event in reader:
            print_event(event, args.format)
            sys.stdout.flush()
    return 0


def cmd_record(args: argparse.Namespace) -> int:
    if args.csv is None and args.jsonl is None:
        raise SystemExit("record requires --csv and/or --jsonl")

    csv_rec = CsvRecorder(args.csv) if args.csv else None
    jsonl_rec = JsonlRecorder(args.jsonl) if args.jsonl else None
    started = time.monotonic()
    batch_count = 0
    sample_count = 0

    try:
        if csv_rec:
            csv_rec.open()
        if jsonl_rec:
            jsonl_rec.open()
        with WirelessReader(args.port, baudrate=args.baudrate) as reader:
            while time.monotonic() - started < args.duration:
                event = reader.read_event(timeout_s=0.2)
                if event is None:
                    continue
                if jsonl_rec:
                    jsonl_rec.write(event)
                if isinstance(event, BatchEvent):
                    batch_count += 1
                    sample_count += event.sample_count
                    if csv_rec:
                        csv_rec.write(event)
        print(f"recorded batches={batch_count} samples={sample_count}")
    finally:
        if csv_rec:
            csv_rec.close()
        if jsonl_rec:
            jsonl_rec.close()
    return 0


def cmd_send(command: str, args: argparse.Namespace) -> int:
    with WirelessReader(args.port, baudrate=args.baudrate) as reader:
        if command == "pair":
            reader.pair()
        elif command == "clear":
            reader.clear()
        elif command == "status":
            reader.request_status()

        until = time.monotonic() + args.listen
        while time.monotonic() < until:
            event = reader.read_event(timeout_s=0.2)
            if event is None:
                continue
            print_event(event, "text")
    return 0


def print_event(event: BatchEvent | BatteryEvent | StatusEvent, fmt: str) -> None:
    if fmt == "jsonl":
        row = asdict(event)
        if isinstance(event, BatchEvent):
            row["samples"] = event.samples.tolist()
        print(json.dumps(row, separators=(",", ":")))
        return

    if isinstance(event, BatchEvent):
        print(
            f"batch dev={event.device_id} fs={event.sample_rate_hz} seq={event.sequence} "
            f"first={event.first_sample_index} samples={event.sample_count} lost={event.lost_packets} "
            f"min={event.samples.min()} max={event.samples.max()}"
        )
    elif isinstance(event, BatteryEvent):
        print(
            f"battery dev={event.device_id} pct={event.battery_percent} "
            f"mv={event.battery_mv} adc_mv={event.adc_mv} raw={event.raw} seq={event.sequence}"
        )
    else:
        print(event.text)


if __name__ == "__main__":
    raise SystemExit(main())
