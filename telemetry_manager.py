#!/usr/bin/env python3
from pymavlink import mavutil
import threading
import time
from agent_telemetry import AgentTelemetry


class TelemetryManager:
    def __init__(self, system_address, agent):
        self.system_address = system_address
        self.agent = agent
        self.run()

    def get_sensor_reading(self, connection):
        while True:
            sensor_reading_msg = connection.recv_match(
                type="NAMED_VALUE_FLOAT", blocking=True
            )
            self.agent.set_sensor_reading(sensor_reading_msg.value)

    def get_geodetic_position(self, connection):
        while True:
            geodetic_position_msg = connection.recv_match(
                type="GLOBAL_POSITION_INT", blocking=True
            )
            self.agent.set_geodetic_position(
                (
                    geodetic_position_msg.lat,
                    geodetic_position_msg.lon,
                    geodetic_position_msg.alt,
                )
            )

    def print_loop(self):
        while True:
            print("CO reading: ", self.agent.get_sensor_reading())
            print("Geodetic position: ", self.agent.get_geodetic_position())
            time.sleep(1)

    def run(self):
        # system_address = "/dev/ttyACM0" #direct USB to pixhawk
        # system_address = "/dev/ttyUSB1" #USB to telemetry radio
        connection = mavutil.mavlink_connection(self.system_address, 57600)

        # Wait for the first heartbeat
        connection.wait_heartbeat()
        print(
            "Heartbeat from system (system %u component %u)"
            % (connection.target_system, connection.target_component)
        )

        # Request all parameters
        connection.mav.request_data_stream_send(
            connection.target_system,
            connection.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_ALL,
            1,
            1,
        )

        # Spawn threads to read sensor readings and geodetic position
        sensor_reading_thread = threading.Thread(
            target=self.get_sensor_reading,
            args=(connection,),
        )
        sensor_reading_thread.start()

        geodetic_position_thread = threading.Thread(
            target=self.get_geodetic_position,
            args=(connection,),
        )
        geodetic_position_thread.start()

        # Spawn thread to print sensor readings and geodetic position
        print_thread = threading.Thread(target=self.print_loop, args=())
        print_thread.start()
