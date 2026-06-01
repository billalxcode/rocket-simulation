from dataclasses import dataclass, field


@dataclass
class ObjectEnvironment:
    name: str = field(default="Generic Environment")
    gravity: float = field(default=0.0)
    density: float = field(default=0.0)
    radius: float = field(default=0.0)


@dataclass
class AtmosphereLayer:
    name: str = field(default="Generic Atmosphere")

    altitude_range: tuple[float, float] = field(default=(0, 0))
    temperature_range: tuple[float, float] = field(default=(0, 0))
    presure_range: tuple[float, float] = field(default=(0, 0))
    density_range: tuple[float, float] = field(default=(0, 0))
    humidity_range: tuple[float, float] = field(default=(0, 0))


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
