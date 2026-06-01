from src.vehicle.rocket import Rocket
from src.vehicle.stage import RocketStage

stage_1 = RocketStage(
    name="S-IC (First Stage)",
    dry_mass=131000.0,  # 131 Metric Ton
    propellant_mass=2140000.0,  # 2,14 Juta kg LOX/RP-1
    thrust_sea_level=34500000.0,  # 34,5 Meganewton
    thrust_vacuum=34500000.0,
    isp_sea_level=263.0,  # Dioptimalkan untuk atmosfer bawah
    isp_vacuum=263.0,
)

# 2. Stage 2: S-II (Sustainer Tengah)
stage_2 = RocketStage(
    name="S-II (Second Stage)",
    dry_mass=360000.0,  # 36 Metric Ton
    propellant_mass=444000.0,  # 444 Ribu kg LOX/LH2
    thrust_sea_level=0.0,
    thrust_vacuum=5165000.0,  # 5,16 Meganewton (Hampa Udara)
    isp_sea_level=0.0,
    isp_vacuum=421.0,  # Efisiensi tinggi menggunakan hidrogen cair
)

# 3. Stage 3: S-IVB (Orbit & Trans-Lunar Injection)
stage_3 = RocketStage(
    name="S-IVB (Third Stage)",
    dry_mass=133000.0,  # 13,3 Metric Ton
    propellant_mass=106600.0,  # 106,6 Ribu kg LOX/LH2
    thrust_sea_level=0.0,
    thrust_vacuum=1033000.0,  # 1,03 Meganewton (Hampa Udara)
    isp_sea_level=0.0,
    isp_vacuum=421.0,  # Efisiensi tinggi untuk manuver luar angkasa
)


class SaturnVRocket(Rocket):
    def __init__(self, name: str = "Saturn V") -> None:
        super().__init__(name=name, stages=[stage_1, stage_2, stage_3])
