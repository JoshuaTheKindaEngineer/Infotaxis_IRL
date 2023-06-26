#!/usr/bin/env python3
from pymavlink import mavutil
from pymavlink import mavwp
import threading
import time
from agent_telemetry import AgentTelemetry
import sys


class TelemetryManager:
    def __init__(self, system_address, agent):
        self.system_address = system_address
        self.agent = agent
        self.run()

    # def get_sensor_reading(self, connection):
    #     while True:
    #         sensor_reading_msg = connection.recv_match(
    #             type="NAMED_VALUE_FLOAT", blocking=True
    #         )
    #         print(sensor_reading_msg.value)
    #         self.agent.set_sensor_reading(sensor_reading_msg.value)

    # def get_geodetic_position(self, connection):
    #     while True:
    #         geodetic_position_msg = connection.recv_match(
    #             type="GLOBAL_POSITION_INT", blocking=True
    #         )
    #         self.agent.set_geodetic_position(
    #             (
    #                 geodetic_position_msg.lat,
    #                 geodetic_position_msg.lon,
    #                 geodetic_position_msg.alt,
    #             )
    #         )

    def handle_message(self, connection):
        while True:
            msg = connection.recv_match(blocking=True)
            if not msg:
                return
            if msg.get_type() == "BAD_DATA":
                if mavutil.all_printable(msg.data):
                    sys.stdout.write(msg.data)
                    sys.stdout.flush()
            if msg.get_type() == "NAMED_VALUE_FLOAT":
                print("CO ppb:", msg.value)
                self.agent.set_sensor_reading(msg.value)
            elif msg.get_type() == "GLOBAL_POSITION_INT":
                self.agent.set_geodetic_position(
                    [
                        msg.lat,
                        msg.lon,
                        msg.alt,
                    ]
                )
            else:
                continue

    # def print_loop(self):
    #     while True:
    #         print("CO reading: ", self.agent.get_sensor_reading())
    #         print("Geodetic position: ", self.agent.get_geodetic_position())
    #         time.sleep(1)

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
        # sensor_reading_thread = threading.Thread(
        #     target=self.get_sensor_reading,
        #     args=(connection,),
        # )
        # sensor_reading_thread.start()

        # geodetic_position_thread = threading.Thread(
        #     target=self.get_geodetic_position,
        #     args=(connection,),
        # )
        # geodetic_position_thread.start()

        msg_handler_thread = threading.Thread(
            target=self.handle_message,
            args=(connection,),
        )
        msg_handler_thread.start()

        # Spawn thread to print sensor readings and geodetic position
        # print_thread = threading.Thread(target=self.print_loop, args=())
        # print_thread.start()
    def set_position(self,new_north,new_east,new_down,type_mask=0b110111111000):
        connection = mavutil.mavlink_connection(self.system_address, 57600)
        waypoint_reached = False
        connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_ned_message(10,connection.target_system,connection.target_component,mavutil.mavlink.MAV_FRAME_LOCAL_NED,type_mask,new_north, new_east, new_down, 0, 0, 0, 0, 0, 0, 0, 0))
        waypoint_distance = 100
        while waypoint_distance>0:
            msg = connection.recv_match(
                type="NAV_CONTROLLER_OUTPUT", blocking=True)
            waypoint_distance = msg.wp_dist
            print("waypoint distance: ", waypoint_distance)
            time.sleep(1)

        if waypoint_distance == 0:
            waypoint_reached = True
            print("waypoint reached")

        return waypoint_reached
