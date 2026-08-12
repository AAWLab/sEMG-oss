from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BatchEvent:
    type: str
    device_id: int
    network_id: int
    sequence: int
    first_sample_index: int
    sample_count: int
    sample_rate_hz: int
    flags: int
    samples: np.ndarray
    lost_packets: int
    timestamp_host_s: float


@dataclass(frozen=True)
class BatteryEvent:
    type: str
    device_id: int
    network_id: int
    sequence: int
    uptime_ms: int
    raw: int
    adc_mv: int
    battery_mv: int
    battery_percent: int
    timestamp_host_s: float


@dataclass(frozen=True)
class StatusEvent:
    type: str
    text: str
    timestamp_host_s: float
