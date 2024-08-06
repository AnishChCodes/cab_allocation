import datetime
from constants import TIME_PER_KM
from utilities import haversine_distance


class Ride:
    def __init__(self, pickup_location: tuple, pickup_time: float, drop_off_location: tuple, pickup_address: str = "",
                 drop_off_address: str = "", buffer: int = 15):
        self.pickup_location = pickup_location  # Tuple of latitude/longitude
        self.pickup_time = pickup_time
        self.pickup_address = pickup_address
        self.drop_off_location = drop_off_location  # Tuple of latitude/longitude
        self.drop_off_address = drop_off_address
        self.buffer = buffer  # Buffer time for each ride in  minutes, default is 15 minutes
        # Taking displacement here rather than actual distance, in real world scenario direct map apis can be used to
        # get the same
        self.displacement = haversine_distance(self.pickup_location[0], self.pickup_location[1],
                                               self.drop_off_location[0], self.drop_off_location[1])
        self.estimated_duration = self._calculate_ride_eta()  # This duration will be travelling time + buffer time
        self.drop_off_time = self._get_drop_off_time()
        self.assigned_driver = None

    def assign_driver(self, driver):
        self.assigned_driver = driver

    def update_buffer(self, buffer):
        self.buffer = buffer

    def _calculate_ride_eta(self) -> float:
        only_ride_eta = int(self.displacement * TIME_PER_KM)
        ride_based_buffer = only_ride_eta * 0.33
        self.buffer = ride_based_buffer if ride_based_buffer > self.buffer else self.buffer

        return self.buffer + only_ride_eta

    def _get_drop_off_time(self) -> float:
        pickup_time_dt = datetime.datetime.fromtimestamp(self.pickup_time)
        drop_off_time_dt = pickup_time_dt + datetime.timedelta(minutes=self.estimated_duration)
        return drop_off_time_dt.timestamp()
