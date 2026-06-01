import time
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
    # Status Mesin Roket (On/Off)
    engine_on: bool = True

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
    delta_time: float = 0.01

    # Massa Bahan Bakarr Roket Saat Ini (kg)
    fuel_massa: float = 30


@dataclass
class RocketStateHistory:
    delta_time: list[float] = field(default_factory=list)
    height: list[float] = field(default_factory=list)
    height_in_km: list[float] = field(default_factory=list)
    velocity: list[float] = field(default_factory=list)
    acceleration: list[float] = field(default_factory=list)
    massa_total: list[float] = field(default_factory=list)
    weight: list[float] = field(default_factory=list)
    total_force: list[float] = field(default_factory=list)
    fuel_massa: list[float] = field(default_factory=list)

    def append(self, state: RocketState):
        self.delta_time.append(state.delta_time)
        self.height.append(state.height)
        self.height_in_km.append(state.height / 1000)
        self.velocity.append(state.velocity)
        self.acceleration.append(state.acceleration)
        self.massa_total.append(state.massa_total)
        self.weight.append(state.weight)
        self.total_force.append(state.total_force)
        self.fuel_massa.append(state.fuel_massa)

    def clear(self):
        self.delta_time.clear()
        self.height.clear()
        self.height_in_km.clear()
        self.velocity.clear()
        self.acceleration.clear()
        self.massa_total.clear()
        self.weight.clear()
        self.total_force.clear()
        self.fuel_massa.clear()

    def average_data(self):
        if len(self.delta_time) == 0:
            return None
        return {
            "delta_time": sum(self.delta_time) / len(self.delta_time),
            "height": sum(self.height) / len(self.height),
            "velocity": sum(self.velocity) / len(self.velocity),
            "acceleration": sum(self.acceleration) / len(self.acceleration),
            "massa_total": sum(self.massa_total) / len(self.massa_total),
            "weight": sum(self.weight) / len(self.weight),
            "total_force": sum(self.total_force) / len(self.total_force),
            "fuel_massa": sum(self.fuel_massa) / len(self.fuel_massa),
        }


class RocketPhysicsCalculator:
    @staticmethod
    def calculate_weight(massa: float, gravity: float):
        return massa * gravity

    @staticmethod
    def calculate_total_force(thrust: float, weight: float):
        return thrust - weight

    @staticmethod
    def calculate_acceleration(total_force: float, massa: float):
        if massa == 0:
            return 0
        return total_force / massa

    @staticmethod
    def calculate_velocity(velocity: float, acceleration: float, delta_time: float):
        return velocity + (acceleration * delta_time)

    @staticmethod
    def calculate_current_height(height: float, velocity: float, delta_time: float):
        return height + (velocity * delta_time)

    @staticmethod
    def calculate_current_fuel_massa(fuel_massa: float, mdot: float, delta_time: float):
        if fuel_massa <= 0:
            return 0
        return fuel_massa - (mdot * delta_time)

    @staticmethod
    def calculate_current_massa(massa_dry: float, massa_fuel: float):
        return massa_dry + massa_fuel


def draw_plots(states: RocketStateHistory, total_time: float, total_iteration: float):
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(14, 8))
    fig.suptitle(
        f"Rocket Simulation - {total_time:.2f}s time - {int(total_iteration)} iteration",
        fontsize=16,
        fontweight="bold",
    )
    iterations = range(len(states.delta_time))

    axes[0, 0].plot(iterations, states.height_in_km, "b-")
    axes[0, 0].set_title("Height (km)")

    axes[0, 1].plot(iterations, states.velocity, "g-")
    axes[0, 1].set_title("Velocity (m/s)")

    axes[0, 2].plot(iterations, states.acceleration, "r-")
    axes[0, 2].set_title("Acceleration (m/s^2)")

    axes[1, 0].plot(iterations, states.massa_total, "c-")
    axes[1, 0].set_title("Massa Total (kg)")

    axes[1, 1].plot(iterations, states.weight, "m-")
    axes[1, 1].set_title("Weight (N)")

    axes[1, 2].plot(iterations, states.total_force, "y-")
    axes[1, 2].set_title("Total Force (N)")

    axes[2, 0].plot(iterations, states.fuel_massa, "b-")
    axes[2, 0].set_title("Fuel Mass (kg)")

    for ax in axes.flat:
        ax.grid(True)
        ax.set_xlabel("Iteration")

    plt.tight_layout()
    plt.show()


def main():
    constants = RocketConstants()
    state = RocketState()
    state_histories = RocketStateHistory()
    state_histories_temporaries = RocketStateHistory()

    simulation_time = 0
    iteration = 50_000

    start_time = time.time()
    for i in range(iteration):
        weight = RocketPhysicsCalculator.calculate_weight(
            massa=state.massa_total, gravity=constants.gravity
        )
        state.weight = weight

        total_force = RocketPhysicsCalculator.calculate_total_force(
            thrust=constants.thrust, weight=state.weight
        )
        state.total_force = total_force

        acceleration = RocketPhysicsCalculator.calculate_acceleration(
            total_force=state.total_force, massa=state.massa_total
        )
        state.acceleration = acceleration

        velocity = RocketPhysicsCalculator.calculate_velocity(
            velocity=state.velocity,
            acceleration=state.acceleration,
            delta_time=state.delta_time,
        )
        state.velocity = velocity

        rocket_height = RocketPhysicsCalculator.calculate_current_height(
            height=state.height, velocity=state.velocity, delta_time=state.delta_time
        )
        state.height = rocket_height

        fuel_massa = RocketPhysicsCalculator.calculate_current_fuel_massa(
            fuel_massa=state.fuel_massa,
            mdot=constants.mdot,
            delta_time=state.delta_time,
        )
        state.fuel_massa = fuel_massa

        massa_total = RocketPhysicsCalculator.calculate_current_massa(
            massa_dry=constants.massa_dry, massa_fuel=state.fuel_massa
        )
        state.massa_total = massa_total

        state_histories.append(state)
        state_histories_temporaries.append(state=state)
        if len(state_histories_temporaries.delta_time) >= 100:
            average_data = state_histories_temporaries.average_data()
            state_histories_temporaries.clear()
            if average_data is not None:
                console.print(
                    f"Rata-rata 100 iterasi terakhir - Time: {average_data['delta_time']:.5f}s - Height: {average_data['height']:.2f} m - Velocity: {average_data['velocity']:.2f} m/s - Acceleration: {average_data['acceleration']:.2f} m/s² - Massa Total: {average_data['massa_total']:.2f} kg - Weight: {average_data['weight']:.2f} N - Total Force: {average_data['total_force']:.2f} N - Fuel Mass: {average_data['fuel_massa']:.2f} kg"
                )

        if state.engine_on is True and state.fuel_massa <= 0:
            constants.thrust = 0
            state.fuel_massa = 0
            state.engine_on = False
            console.print("Roket kehabisan bahan bakar")
            break

        if state.engine_on is False and state.height <= 0:
            constants.thrust = 0
            state.height = 0
            state.engine_on = False
            console.print("Roket berada di tanah")
            break
    
    end_time = time.time()
    simulation_time = end_time - start_time
    draw_plots(state_histories, simulation_time, iteration)


if __name__ == "__main__":
    main()
