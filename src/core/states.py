import numpy as np
from dataclasses import dataclass
from src.environments.generic import GenericEnvironment


@dataclass
class State:
    time: float
    position: np.ndarray
    velocity: np.ndarray
    total_mass: float
    altitude: float
    environment: GenericEnvironment
