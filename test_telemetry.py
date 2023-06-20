from telemetry_manager import TelemetryManager
from agent_telemetry import AgentTelemetry


def run():
    agent_telemetry = AgentTelemetry([0, 0, 0])
    telemetry_manager = TelemetryManager("/dev/ttyUSB0", agent_telemetry)


if __name__ == "__main__":
    run()
