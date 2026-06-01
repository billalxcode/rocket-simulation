from src.environments.generic import AtmosphereLayer

throposphere = AtmosphereLayer(
    name="Trophosphere",
    altitude_range=(0.0, 12.0),  # in km
    temperature_range=(15.0, -56.0),  # in celcius
    presure_range=(1013.25, 200.0),  # in hpa
    humidity_range=(0.0, 100.0),  # in pct (percentage)
)
stratosphere = AtmosphereLayer(
    name="Stratosphere",
    altitude_range=(12.0, 50.0),
    temperature_range=(-56.0, 0.0),
    presure_range=(200.0, 1.0),
    humidity_range=(0.0, 0.01),
)
mesonsphere = AtmosphereLayer(
    name="Mesonsphere",
    altitude_range=(50.0, 85.0),
    temperature_range=(0.0, -90.0),
    presure_range=(1.0, 0.01),
    humidity_range=(0.0, 0.0),
)
thermosphere = AtmosphereLayer(
    name="Thermosphere",
    altitude_range=(85.0, 600.0),
    temperature_range=(-90.0, 1500.0),
    presure_range=(0.01, 0.00001),
    humidity_range=(0.0, 0.0)
)
exosphere = AtmosphereLayer(
    name="Exosphere",
    altitude_range=(600.0, float('inf'))
)


class Atmosphere:
    def __init__(self) -> None:
        pass
