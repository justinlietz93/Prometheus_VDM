from dataclasses import dataclass

@dataclass
class PortSpec:
    name: str
    direction: str
    enabled: bool = True
