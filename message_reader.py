#!/usr/bin/env python3
from pymavlink import mavutil
import threading
import time
from agent_telemetry import AgentTelemetry


# def handle_heartbeat(msg):
#     mode = mavutil.mode_string_v10(msg)
#     is_armed = msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
#     is_enabled = msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_GUIDED_ENABLED

# def read_loop(connection):
#     while True:
#         # grab a mavlink message
#         print("Waiting for message")
#         msg = connection.recv_match(blocking=False)
#         if not msg:
#             print("No message")
#             return

#         # handle the message based on its type
#         msg_type = msg.get_type()
#         if msg_type == "BAD_DATA":
#             if mavutil.all_printable(msg.data):
#                 sys.stdout.write(msg.data)
#                 sys.stdout.flush()
#         elif msg_type == "RC_CHANNELS_RAW":
#             handle_rc_raw(msg)
#         elif msg_type == "HEARTBEAT":
#             handle_heartbeat(msg)
#         elif msg_type == "VFR_HUD":
#             handle_hud(msg)
#         elif msg_type == "ATTITUDE":
#             handle_attitude(msg)

def read_loop(connection, agent):
    while True:
        sensor_reading_msg = connection.recv_match(type='NAMED_VALUE_FLOAT', blocking=True)
        agent.set_sensor_reading(sensor_reading_msg.value)
        print(sensor_reading_msg.name)
        
def print_loop(agent):
    while True:
        print("CO reading: ", agent.get_sensor_reading())
        time.sleep(1)


def main():
    agent = AgentTelemetry()
    system_address = "/dev/ttyACM0"  # default address for SITL
    connection = mavutil.mavlink_connection(system_address, 57600)

    # Wait for the first heartbeat
    connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (connection.target_system, connection.target_component))

    # enter the data loop
    read_thread = threading.Thread(target=read_loop, args=(connection, agent,))
    read_thread.start()
    
    print_thread = threading.Thread(target=print_loop, args=(agent,))
    print_thread.start()
    #read_loop(connection, agent)


if __name__ == "__main__":
    main()
