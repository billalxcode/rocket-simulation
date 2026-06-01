import math
from dataclasses import dataclass, field
from src.environments.generic import ObjectEnvironment, earth


@dataclass
class RocketStage:
    name: str = field(default="Stage")
    dry_mass: float = field(default=0.0)  # kg (Massa struktur, mesin, tangki kosong)
    propellant_mass: float = field(default=0.0)  # kg (Massa bahan bakar + oksidator)
    thrust_vacuum: float = field(default=0.0)  # Newton (Gaya dorong di luar angkasa)
    thrust_sea_level: float = field(default=0.0)  # Newton (Gaya dorong di bumi)
    isp_vacuum: float = field(default=0.0)  # detik (Efisiensi di luar angkasa)
    isp_sea_level: float = field(default=0.0)  # detik (Efisiensi di bumi)
    environment: ObjectEnvironment = field(default=earth)

    @property
    def initial_mass(self) -> float:
        return self.dry_mass + self.propellant_mass

    @property
    def mass_ratio(self) -> float:
        return self.initial_mass / self.dry_mass

    @property
    def structural_ratio(self):
        return self.dry_mass / self.initial_mass

    @property
    def propellant_fraction(self):
        return self.propellant_mass / self.initial_mass

    @property
    def delta_v_ideal(self):
        ln = math.log(self.mass_ratio)
        return self.isp_vacuum * self.environment.gravity * ln

    @property
    def mass_flow_rate(self):
        return self.thrust_vacuum / (self.isp_vacuum * self.environment.gravity)

    @property
    def burn_time(self):
        return self.propellant_mass / self.mass_flow_rate

    @property
    def thrust2weight_Ratio(self):
        return self.thrust_vacuum / (self.initial_mass / self.environment.gravity)

    def get_instantaneous_mass(self, delta_time: float):
        return self.initial_mass - (self.mass_flow_rate * delta_time)

    def get_acceleration(self, delta_time: float):
        # TODO: add drag
        return self.thrust_vacuum / self.initial_mass

    @property
    def net_liffoff_acceleration(self):
        return (
            self.thrust_vacuum
            - (self.initial_mass * self.environment.gravity) / self.initial_mass
        )

    @property
    def get_thrust_interpolation_preasure(self):
        pass

    def consume(self):
        pass
