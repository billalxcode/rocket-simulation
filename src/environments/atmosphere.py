from src.environments.generic import AtmosphereLayer

troposphere = AtmosphereLayer(
    name="Troposphere",
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
mesosphere = AtmosphereLayer(
    name="Mesosphere",
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
    humidity_range=(0.0, 0.0),
)
exosphere = AtmosphereLayer(
    name="Exosphere",
    altitude_range=(600.0, float("inf")),
    temperature_range=(
        1500.0,
        1500.0,
    ),
    presure_range=(0.00001, 0.0),
    humidity_range=(0.0, 0.0),
)
