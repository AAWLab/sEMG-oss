from __future__ import annotations

import struct
import time
from typing import Iterable

import numpy as np

from .events import BatteryEvent, BatchEvent, StatusEvent

MAGIC = 0x32474D45
MAGIC_BYTES = b"EMG2"
VERSION = 1
TYPE_DATA = 4
TYPE_BATTERY = 5
DATA_HEADER_LEN = 26
BATTERY_LEN = 26
MAX_SAMPLE_COUNT = 80
MAX_PACKET_LEN = 250


class PacketParser:
    """Incremental parser for mixed EMG2 binary packets and text status lines."""

    def __init__(self) -> None:
        self._buffer = bytearray()
        self.parse_drops = 0
        self._last_sequence_by_device: dict[int, int] = {}
        self._lost_packets_by_device: dict[int, int] = {}

    def feed(self, data: bytes) -> list[BatchEvent | BatteryEvent | StatusEvent]:
        self._buffer.extend(data)
        return list(self._parse_available())

    def _parse_available(self) -> Iterable[BatchEvent | BatteryEvent | StatusEvent]:
        while self._buffer:
            magic_at = self._buffer.find(MAGIC_BYTES)
            if magic_at < 0:
                yield from self._consume_text_keep_suffix()
                return

            if magic_at > 0:
                yield from self._consume_text(magic_at)

            if len(self._buffer) < 6:
                return

            version = self._buffer[4]
            packet_type = self._buffer[5]
            if version != VERSION:
                del self._buffer[0]
                self.parse_drops += 1
                continue

            if packet_type == TYPE_BATTERY:
                if len(self._buffer) < BATTERY_LEN:
                    return
                packet = bytes(self._buffer[:BATTERY_LEN])
                del self._buffer[:BATTERY_LEN]
                event = self._parse_battery(packet)
                if event is not None:
                    yield event
                continue

            if packet_type != TYPE_DATA:
                del self._buffer[0]
                self.parse_drops += 1
                continue

            if len(self._buffer) < DATA_HEADER_LEN:
                return

            header = bytes(self._buffer[:DATA_HEADER_LEN])
            fields = struct.unpack("<IBBBBIIIHHH", header)
            _, _, _, device_id, channel_count, network_id, sequence, first_sample_index, sample_count, sample_rate_hz, flags = fields

            if channel_count != 1 or sample_count < 1 or sample_count > MAX_SAMPLE_COUNT or sample_rate_hz < 1:
                del self._buffer[0]
                self.parse_drops += 1
                continue

            packet_len = DATA_HEADER_LEN + sample_count * channel_count * 2
            if packet_len > MAX_PACKET_LEN:
                del self._buffer[0]
                self.parse_drops += 1
                continue
            if len(self._buffer) < packet_len:
                return

            packet = bytes(self._buffer[:packet_len])
            del self._buffer[:packet_len]
            yield self._parse_data_packet(
                packet,
                device_id=device_id,
                network_id=network_id,
                sequence=sequence,
                first_sample_index=first_sample_index,
                sample_count=sample_count,
                sample_rate_hz=sample_rate_hz,
                flags=flags,
            )

    def _consume_text_keep_suffix(self) -> Iterable[StatusEvent]:
        keep = min(3, len(self._buffer))
        text_len = len(self._buffer) - keep
        if text_len <= 0:
            return []
        events = list(self._consume_text(text_len))
        return events

    def _consume_text(self, length: int) -> Iterable[StatusEvent]:
        raw = bytes(self._buffer[:length])
        del self._buffer[:length]
        text = raw.decode("utf-8", errors="ignore")
        lines = [line.strip() for line in text.replace("\r", "\n").split("\n")]
        now = time.time()
        for line in lines:
            if line:
                yield StatusEvent(type="status", text=line, timestamp_host_s=now)

    def _parse_data_packet(
        self,
        packet: bytes,
        *,
        device_id: int,
        network_id: int,
        sequence: int,
        first_sample_index: int,
        sample_count: int,
        sample_rate_hz: int,
        flags: int,
    ) -> BatchEvent:
        samples = np.frombuffer(packet, dtype="<i2", count=sample_count, offset=DATA_HEADER_LEN).copy()
        lost = self._lost_packets_by_device.get(device_id, 0)
        last_sequence = self._last_sequence_by_device.get(device_id)
        if last_sequence is not None and sequence > last_sequence + 1:
            lost += sequence - last_sequence - 1
        self._last_sequence_by_device[device_id] = sequence
        self._lost_packets_by_device[device_id] = lost
        return BatchEvent(
            type="batch",
            device_id=device_id,
            network_id=network_id,
            sequence=sequence,
            first_sample_index=first_sample_index,
            sample_count=sample_count,
            sample_rate_hz=sample_rate_hz,
            flags=flags,
            samples=samples,
            lost_packets=lost,
            timestamp_host_s=time.time(),
        )

    def _parse_battery(self, packet: bytes) -> BatteryEvent | None:
        magic, version, packet_type, device_id, battery_percent, network_id, sequence, uptime_ms, raw, adc_mv, battery_mv = struct.unpack(
            "<IBBBBIIIHHH", packet
        )
        if magic != MAGIC or version != VERSION or packet_type != TYPE_BATTERY:
            self.parse_drops += 1
            return None
        if device_id == 0 or battery_percent > 100:
            self.parse_drops += 1
            return None
        return BatteryEvent(
            type="battery",
            device_id=device_id,
            network_id=network_id,
            sequence=sequence,
            uptime_ms=uptime_ms,
            raw=raw,
            adc_mv=adc_mv,
            battery_mv=battery_mv,
            battery_percent=battery_percent,
            timestamp_host_s=time.time(),
        )
