import datetime

from constants import TIME_PER_KM
from utilities import haversine_distance
from uuid import UUID


class Driver:
    def __init__(self, driver_price: int, current_location: tuple,
                 next_availability: float):
        self.driver_price = driver_price
        self.expected_next_location = current_location
        self.expected_next_availability = next_availability
        self.assigned_rides = []

    def assign_ride(self, ride):
        self.assigned_rides.append(ride)

    def calculate_pickup_distance(self, pickup_location):
        displacement = haversine_distance(self.expected_next_location[0], self.expected_next_location[1],
                                          pickup_location[0], pickup_location[1])
        return displacement

    def calculate_pickup_cost(self, pickup_location):
        displacement = self.calculate_pickup_distance(pickup_location)
        pickup_cost = self.driver_price * displacement
        return pickup_cost

    def calculate_pickup_time(self, pickup_location) -> float:
        time_to_reach = int(self.calculate_pickup_distance(pickup_location) * TIME_PER_KM)
        pickup_time_dt = (datetime.datetime.fromtimestamp(self.expected_next_availability) +
                          datetime.timedelta(minutes=time_to_reach))
        return pickup_time_dt.timestamp()

    def driver_available(self, pickup_location, pickup_time):
        return self.calculate_pickup_time(pickup_location) <= pickup_time
