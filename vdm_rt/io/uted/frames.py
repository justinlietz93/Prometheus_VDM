from dataclasses import dataclass

@dataclass
class SensorFrame:
    tick: int
    port: str
    payload: dict
    timestamp_us: int

@dataclass
class ActuatorFrame:
    tick: int
    port: str
    payload: dict
    timestamp_us: int
