import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from rich.console import Console

console = Console()


@dataclass
class RocketConstants:
    # Gravitasi bumi (m/s^2)
    gravity: float = 9.81

    # Thrust mesin roket (Newton)
    thrust: float = 2300  # 2.3 Meter Newton

    # Laju Konsumsi Bahan Bakar (kg/s)
    mdot: float = 0.5

    # Massa Kosong Roket Tanpa Bahan Bakar (kg)
    massa_dry: float = 20.0


@dataclass
class RocketState:
    # Ketinggian roket dari tanah (m)
    height: float = 0.0

    # Kecepatan Vertikal Roket (m/s)
    velocity: float = 0.0

    # Percepatan Roket (m/s^2)
    acceleration: float = 0.0

    # Massa Total Roket Saat ini (kg)
    massa_total: float = 50.0

    # Berat pada Roket
    weight: float = 0.0

    # Gaya Total
    total_force: float = 0

    # Waktu simulasi
    delta_time: float = 0.0

    # Massa Bahan Bakarr Roket Saat Ini (kg)
    fuel_massa: float = 30


@dataclass
class RocketStateHistory:
    delta_time: list[float] = field(default_factory=list)
    height: list[float] = field(default_factory=list)
    velocity: list[float] = field(default_factory=list)
    acceleration: list[float] = field(default_factory=list)
    massa_total: list[float] = field(default_factory=list)
    weight: list[float] = field(default_factory=list)
    total_force: list[float] = field(default_factory=list)

    def append(self, state: RocketState):
        self.delta_time.append(state.delta_time)
        self.height.append(state.height)
        self.velocity.append(state.velocity)
        self.acceleration.append(state.acceleration)
        self.massa_total.append(state.weight)
        self.weight.append(state.weight)
        self.total_force.append(state.total_force)


class RocketPhysicsCalculator:
    @staticmethod
    def calculate_weight(massa: float, gravity: float):
        return massa * gravity

    @staticmethod
    def calculate_total_force(thrust: float, weight: float):
        return thrust - weight

    @staticmethod
    def calculate_acceleration(total_force: float, massa: float):
        return total_force / massa

    @staticmethod
    def calculate_velocity(velocity: float, acceleration: float, delta_time: float):
        return velocity + (acceleration * delta_time)

    @staticmethod
    def calculate_current_height(height: float, velocity: float, delta_time: float):
        return height + (velocity * delta_time)

    @staticmethod
    def calculate_current_massa(massa: float, mdot: float, delta_time: float):
        return massa - (mdot * delta_time)


def draw_plots(states: RocketStateHistory):
    print(states.delta_time)
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(14, 8))
    fig.suptitle("Rocket Simulation", fontsize=16, fontweight="bold")

    axes[0, 0].plot(states.delta_time, states.height, "b-")
    axes[0, 0].set_title("Height (m)")

    axes[0, 1].plot(states.delta_time, states.velocity, "g-")
    axes[0, 1].set_title("Velocity (m/s)")

    axes[0, 2].plot(states.delta_time, states.acceleration, "r-")
    axes[0, 2].set_title("Acceleration (m/s^2)")

    axes[1, 0].plot(states.delta_time, states.massa_total, "c-")
    axes[1, 0].set_title("Massa Total (kg)")

    axes[1, 1].plot(states.delta_time, states.weight, "m-")
    axes[1, 1].set_title("Weight (N)")

    axes[1, 2].plot(states.delta_time, states.total_force, "y-")
    axes[1, 2].set_title("Total Force (N)")

    for ax in axes.flat:
        ax.grid(True)
        ax.set_xlabel("Delta Time (s)")

    plt.tight_layout()
    plt.show()


def main():
    constants = RocketConstants()
    state = RocketState()
    state_histories = RocketStateHistory()
    start_time = time.time()

    total_time = 2
    delay_simulation = 0.005

    for i in range(int(total_time / delay_simulation)):
        end_time = time.time()

        delta_time = end_time - start_time
        state.delta_time = delta_time

        weight = RocketPhysicsCalculator.calculate_weight(
            state.massa_total, constants.gravity
        )
        state.weight = weight
        console.print("Berat Roket", weight, "kg")

        total_force = RocketPhysicsCalculator.calculate_total_force(
            constants.thrust, state.weight
        )
        state.total_force = total_force
        console.print("Gaya Total", total_force, "newton")

        acceleration = RocketPhysicsCalculator.calculate_acceleration(
            state.total_force, state.massa_total
        )
        state.acceleration = acceleration
        console.print("Akselerasi", acceleration, "m/s")

        velocity = RocketPhysicsCalculator.calculate_velocity(
            state.velocity, state.acceleration, delta_time=delta_time
        )
        state.velocity = velocity
        console.print("Vertical speed new", velocity, "m/s")

        rocket_height = RocketPhysicsCalculator.calculate_current_height(
            state.height, state.velocity, delta_time=delta_time
        )
        state.height = rocket_height
        console.print("Rocket height", rocket_height, "m")

        massa_total = RocketPhysicsCalculator.calculate_current_massa(
            state.massa_total, constants.mdot, delta_time=delta_time
        )
        state.massa_total = massa_total

        console.print("Massa total", massa_total, "kg")

        if massa_total < constants.massa_dry:
            console.print("Mesin kehabisan bahan bakar")
            constants.thrust = 0

        console.print("=" * 50)
        time.sleep(delay_simulation)

        state_histories.append(state)

    draw_plots(state_histories)


if __name__ == "__main__":
    main()
