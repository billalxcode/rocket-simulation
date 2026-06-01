from src.vehicle.stage import RocketStage


class Rocket:
    def __init__(self, name: str, stages: list[RocketStage] = []) -> None:
        self.name = name
        self.stages: list[RocketStage] = stages

    def add_stage(self, stage: RocketStage) -> None:
        self.stages.append(stage)

    def consume_stages(self):
        for stage in self.stages:
            stage.consume()
