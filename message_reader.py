#!/usr/bin/env python3
from pymavlink import mavutil


def handle_heartbeat(msg):
    mode = mavutil.mode_string_v10(msg)
    is_armed = msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED
    is_enabled = msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_GUIDED_ENABLED


def handle_rc_raw(msg):
    channels = (
        msg.chan1_raw,
        msg.chan2_raw,
        msg.chan3_raw,
        msg.chan4_raw,
        msg.chan5_raw,
        msg.chan6_raw,
        msg.chan7_raw,
        msg.chan8_raw,
    )


def handle_hud(msg):
    hud_data = (
        msg.airspeed,
        msg.groundspeed,
        msg.heading,
        msg.throttle,
        msg.alt,
        msg.climb,
    )


def handle_attitude(msg):
    attitude_data = (
        msg.roll,
        msg.pitch,
        msg.yaw,
        msg.rollspeed,
        msg.pitchspeed,
        msg.yawspeed,
    )


def read_loop(connection):
    while True:
        # grab a mavlink message
        msg = connection.recv_match(blocking=False)
        if not msg:
            return

        # handle the message based on its type
        msg_type = msg.get_type()
        if msg_type == "BAD_DATA":
            if mavutil.all_printable(msg.data):
                sys.stdout.write(msg.data)
                sys.stdout.flush()
        elif msg_type == "RC_CHANNELS_RAW":
            handle_rc_raw(msg)
        elif msg_type == "HEARTBEAT":
            handle_heartbeat(msg)
        elif msg_type == "VFR_HUD":
            handle_hud(msg)
        elif msg_type == "ATTITUDE":
            handle_attitude(msg)


def main():
    system_address = "udpin:localhost:14540"  # default address for SITL
    connection = mavutil.mavlink_connection(system_address)

    # Wait for the first heartbeat
    connection.wait_heartbeat()
    print("Heartbeat received")

    # request data to be sent at the given rate
    connection.mav.request_data_stream_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_ALL,
        1,
        1,
    )

    # enter the data loop
    read_loop(connection)


if __name__ == "__main__":
    main()
