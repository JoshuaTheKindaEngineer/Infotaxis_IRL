import threading

class AgentTelemetry:
    def __init__(self):
        self._sensor_reading = 0
        self._geodetic_position = (0, 0, 0)
        self._relative_position = (0, 0, 0)
        self._lock = threading.Lock()
    
    def get_sensor_reading(self):
        return self._sensor_reading
    
    def get_geodetic_position(self):
        return self._geodetic_position
    
    def get_relative_position(self):
        return self._relative_position
    
    def set_sensor_reading(self, sensor_reading):
        with self._lock:
            self._sensor_reading = sensor_reading
    
    def set_geodetic_position(self, geodetic_position):
        self._geodetic_position = geodetic_position
        
    def set_relative_position(self, relative_position):
        self._relative_position = relative_position