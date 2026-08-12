from __future__ import annotations

import argparse

from aawlab_emg import WirelessReader


def main() -> None:
    parser = argparse.ArgumentParser(description="Print AAW Lab sEMG wireless batches")
    parser.add_argument("--port", required=True)
    args = parser.parse_args()

    with WirelessReader(args.port) as reader:
        for event in reader:
            if event.type == "batch":
                print(
                    f"dev={event.device_id} fs={event.sample_rate_hz} "
                    f"seq={event.sequence} samples={event.samples.tolist()}"
                )
            elif event.type == "battery":
                print(f"battery dev={event.device_id} {event.battery_percent}% {event.battery_mv}mV")
            elif event.type == "status":
                print(event.text)


if __name__ == "__main__":
    main()
