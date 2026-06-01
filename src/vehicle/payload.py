from dataclasses import dataclass


@dataclass
class RocketPayload:
    name: str
    mass: float  # kg
