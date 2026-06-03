from dataclasses import dataclass, field
from src.utils.units import avg


@dataclass
class AtmosphereLayer:
    name: str = field(default="Generic Atmosphere")

    altitude_range: tuple[float, float] = field(default=(0, 0))
    temperature_range: tuple[float, float] = field(default=(0, 0))
    presure_range: tuple[float, float] = field(default=(0, 0))
    density_range: tuple[float, float] = field(default=(0, 0))
    humidity_range: tuple[float, float] = field(default=(0, 0))

    @property
    def avg_altitude(self):
        return avg(self.altitude_range)

    @property
    def avg_temperature(self):
        return avg(self.temperature_range)

    @property
    def avg_presure(self):
        return avg(self.presure_range)

    @property
    def avg_density(self):
        return avg(self.density_range)

    @property
    def avg_humidity(self):
        return avg(self.humidity_range)


@dataclass
class ObjectEnvironment:
    name: str = field(default="Generic Environment")
    gravity: float = field(default=0.0)
    density: float = field(default=0.0)
    radius: float = field(default=0.0)
    atmosphere: AtmosphereLayer = field(default_factory=AtmosphereLayer)


earth = ObjectEnvironment(
    name="Earth",
    gravity=9.81,  # m/s^2
    density=1.225,  # kg/m^3 at sea level
    radius=6371000,  # meters
)

moon = ObjectEnvironment(
    name="Moon",
    gravity=1.62,  # m/s^2
    density=0.0,  # kg/m^3 (negligible atmosphere
    radius=1737000,  # meters
)
