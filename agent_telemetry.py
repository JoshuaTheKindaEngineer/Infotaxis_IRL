import threading
import pymap3d as pm


class AgentTelemetry:
    def __init__(self, reference_point):
        self._sensor_reading = 0
        self._geodetic_position = [0, 0, 0]
        self.reference_point = reference_point
        self._relative_position = [0, 0, 0]  # NED
        self._sensor_reading_lock = threading.Lock()
        self._position_lock = threading.Lock()

    def get_sensor_reading(self):
        return self._sensor_reading

    def get_geodetic_position(self):
        return self._geodetic_position

    def get_relative_position(self):
        return self._relative_position

    def set_sensor_reading(self, sensor_reading):
        with self._sensor_reading_lock:
            self._sensor_reading = sensor_reading

    def set_geodetic_position(self, geodetic_position):
        with self._position_lock:
            self._geodetic_position = geodetic_position
            self.set_relative_position(geodetic_position)

    def set_relative_position(self, geodetic_position):
        self._relative_position = pm.geodetic2ned(
            geodetic_position[0],
            geodetic_position[1],
            geodetic_position[2],
            self.reference_point,
            self.reference_point,
            self.reference_point,
        )
