#!/usr/bin/env python3
from pymavlink import mavutil
import threading
import time
from agent_telemetry import AgentTelemetry

def get_sensor_reading(connection, agent):
    while True:
        sensor_reading_msg = connection.recv_match(type='NAMED_VALUE_FLOAT', blocking=True)
        agent.set_sensor_reading(sensor_reading_msg.value)
        
def get_geodetic_position(connection, agent):
    while True:
        geodetic_position_msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        agent.set_geodetic_position((geodetic_position_msg.lat, geodetic_position_msg.lon, geodetic_position_msg.alt))
        
def print_loop(agent):
    while True:
        print("CO reading: ", agent.get_sensor_reading())
        print("Geodetic position: ", agent.get_geodetic_position())
        time.sleep(1)


def main():
    agent = AgentTelemetry()
    #system_address = "/dev/ttyACM0" #direct USB to pixhawk
    system_address = "/dev/ttyUSB1" #USB to telemetry radio
    connection = mavutil.mavlink_connection(system_address, 57600)

    # Wait for the first heartbeat
    connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (connection.target_system, connection.target_component))
    
    # Request all parameters
    connection.mav.request_data_stream_send(connection.target_system, connection.target_component, 
	mavutil.mavlink.MAV_DATA_STREAM_ALL, 1, 1)

    # Spawn threads to read sensor readings and geodetic position
    sensor_reading_thread = threading.Thread(target=get_sensor_reading, args=(connection, agent,))
    sensor_reading_thread.start()
    
    geodetic_position_thread = threading.Thread(target=get_geodetic_position, args=(connection, agent,))
    geodetic_position_thread.start()
    
    # Spawn thread to print sensor readings and geodetic position
    print_thread = threading.Thread(target=print_loop, args=(agent,))
    print_thread.start()


if __name__ == "__main__":
    main()
