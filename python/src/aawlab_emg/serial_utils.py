from __future__ import annotations

from dataclasses import dataclass

from serial.tools import list_ports


@dataclass(frozen=True)
class SerialPortInfo:
    device: str
    description: str
    hwid: str
    manufacturer: str | None
    product: str | None
    serial_number: str | None


def list_serial_ports() -> list[SerialPortInfo]:
    return [
        SerialPortInfo(
            device=port.device,
            description=port.description,
            hwid=port.hwid,
            manufacturer=port.manufacturer,
            product=port.product,
            serial_number=port.serial_number,
        )
        for port in list_ports.comports()
    ]
