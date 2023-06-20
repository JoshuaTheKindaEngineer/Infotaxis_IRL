#!/usr/bin/env python3
from telemetry_manager import TelemetryManager
from agent_telemetry import AgentTelemetry
from chemotaxis import Chemotaxis
import time
import pymap3d as pm


def run():
    reference_point = (0, 0, 0)
    agent_telemetry = AgentTelemetry(reference_point)
    telemetry_manager = TelemetryManager("/dev/ttyACM0", agent_telemetry)
    chemotaxis = Chemotaxis(0, 0, 0.1)

    while True:
        new_x, new_y = chemotaxis.update(agent_telemetry.get_sensor_reading())
        new_geodetic_position = pm.ned2geodetic(
            new_y,
            new_x,
            agent_telemetry.get_geodetic_position[2],
            agent_telemetry.reference_point[0],
            agent_telemetry.reference_point[1],
            agent_telemetry.reference_point[2],
        )
        # TODO send new geodetic position to pixhawk
        # block until aircraft reaches new position
        time.sleep(
            1
        )  # waiting time for sensor to settle, could be replaced by logic to see if it is changing much


if __name__ == "__main__":
    run()
