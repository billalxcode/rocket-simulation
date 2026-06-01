import numpy as np
from src.core.states import State
from src.environments.generic import earth
from src.vehicle.rockets.saturnv import SaturnVRocket


class App:
    def __init__(self, delta_time: float) -> None:
        self.delta_time = delta_time
        self.state = State(
            time=0.0,
            position=np.zeros(3),
            velocity=np.zeros(3),
            total_mass=0.0,
            altitude=0.0,
            environment=earth,
        )
        self.rocket = SaturnVRocket()

    def update(self) -> None:
        self.state.time += self.delta_time
        self.rocket.consume_stages()


if __name__ == "__main__":
    app = App(delta_time=0.01)
    app.update()
