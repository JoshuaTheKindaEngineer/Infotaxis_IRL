#!/usr/bin/env python3
from telemetry_manager import TelemetryManager
from agent_telemetry import AgentTelemetry
from chemotaxis import Chemotaxis
from csv_logger import CSVLogger
import queue
import time
import pymap3d as pm
import threading

Mode = 0


def run():
    reference_point = (0, 0, 0)
    agent_telemetry = AgentTelemetry(reference_point)
    telemetry_manager = TelemetryManager("/dev/ttyUSB0", agent_telemetry)
    chemotaxis = Chemotaxis(0.1)

    csv_log_queue = queue.Queue()
    csv_logger = CSVLogger()
    csv_thread = threading.Thread(
        target=csv_logger.write_log,
        args=(csv_log_queue, "chemotaxis_experiment_1"),
        daemon=True,
    )
    csv_thread.start()

    experiment_start_time = time.time()
    while True:
        new_north, new_east, new_down = chemotaxis.update(
            agent_telemetry.get_sensor_reading(), agent_telemetry._relative_position
        )
        # new_geodetic_position = pm.ned2geodetic(
        #     new_East,
        #     new_North,
        #     agent_telemetry.get_geodetic_position[2],
        #     agent_telemetry.reference_point[0],
        #     agent_telemetry.reference_point[1],
        #     agent_telemetry.reference_point[2],
        # )
        print("new position: ", new_north, new_east, new_down)

        csv_log_queue.put(
            (
                time.time() - experiment_start_time,
                agent_telemetry.get_sensor_reading(),
                agent_telemetry.get_relative_position()[0],
                agent_telemetry.get_relative_position()[1],
                agent_telemetry.get_relative_position()[2],
                new_north,
                new_east,
                new_down,
            )
        )
        # TODO send new geodetic position to pixhawk
        # block until aircraft reaches new position
        time.sleep(
            1
        )  # waiting time for sensor to settle, could be replaced by logic to see if it is changing much


if __name__ == "__main__":
    run()
