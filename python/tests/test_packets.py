from __future__ import annotations

import struct

from aawlab_emg.events import BatteryEvent, BatchEvent, StatusEvent
from aawlab_emg.packets import MAGIC, TYPE_BATTERY, TYPE_DATA, VERSION, PacketParser


def data_packet(device_id: int = 1, sequence: int = 7, first_sample_index: int = 100, samples: list[int] | None = None) -> bytes:
    if samples is None:
        samples = [-3, -2, -1, 0, 1, 2, 3]
    header = struct.pack(
        "<IBBBBIIIHHH",
        MAGIC,
        VERSION,
        TYPE_DATA,
        device_id,
        1,
        1234,
        sequence,
        first_sample_index,
        len(samples),
        3300,
        0,
    )
    return header + struct.pack("<" + "h" * len(samples), *samples)


def battery_packet() -> bytes:
    return struct.pack(
        "<IBBBBIIIHHH",
        MAGIC,
        VERSION,
        TYPE_BATTERY,
        1,
        87,
        1234,
        2,
        9000,
        2048,
        1971,
        3942,
    )


def test_parse_data_packet() -> None:
    parser = PacketParser()
    events = parser.feed(data_packet())
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, BatchEvent)
    assert event.device_id == 1
    assert event.network_id == 1234
    assert event.sequence == 7
    assert event.first_sample_index == 100
    assert event.sample_rate_hz == 3300
    assert event.samples.tolist() == [-3, -2, -1, 0, 1, 2, 3]


def test_parse_battery_packet() -> None:
    parser = PacketParser()
    events = parser.feed(battery_packet())
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, BatteryEvent)
    assert event.device_id == 1
    assert event.battery_percent == 87
    assert event.battery_mv == 3942


def test_parse_mixed_text_and_packet() -> None:
    parser = PacketParser()
    events = parser.feed(b"\nSTAT state=paired\n" + data_packet(samples=[1, 2]))
    assert len(events) == 2
    assert isinstance(events[0], StatusEvent)
    assert events[0].text == "STAT state=paired"
    assert isinstance(events[1], BatchEvent)
    assert events[1].samples.tolist() == [1, 2]


def test_fragmented_packet() -> None:
    packet = data_packet(samples=[10, 11, 12])
    parser = PacketParser()
    assert parser.feed(packet[:5]) == []
    events = parser.feed(packet[5:])
    assert len(events) == 1
    assert isinstance(events[0], BatchEvent)
    assert events[0].samples.tolist() == [10, 11, 12]


def test_lost_packet_count() -> None:
    parser = PacketParser()
    events = parser.feed(data_packet(sequence=1) + data_packet(sequence=4))
    assert len(events) == 2
    assert isinstance(events[1], BatchEvent)
    assert events[1].lost_packets == 2
