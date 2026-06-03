from typing import Literal

PascalUnit = Literal["pa", "hpa"]


class Pascal:
    def __init__(self, value: float, unit: PascalUnit) -> None:
        self.value = value
        self.unit = unit

    def to_pa(self):
        if self.unit == "pa":
            return self.value
        return self.value / 1000

    def to_hpa(self):
        if self.unit == "hpa":
            return self.value
        return self.value * 1000
