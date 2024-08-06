import random

from datetime import timedelta
from constants import MIN_LATITUDE, MAX_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE, END_TIME, START_TIME, MAX_DRIVER_PRICE, \
    MIN_DRIVER_PRICE
from driver import Driver
from ride import Ride
from ride_manager import RideManager


def generate_random_location():
    latitude = random.uniform(MIN_LATITUDE, MAX_LATITUDE)
    longitude = random.uniform(MIN_LONGITUDE, MAX_LONGITUDE)
    return latitude, longitude


def generate_random_timestamp():
    delta = END_TIME - START_TIME
    seconds = random.randint(0, int(delta.total_seconds()))
    return START_TIME + timedelta(seconds=seconds)


def generate_ride_data_point():
    pickup_location = generate_random_location()
    pickup_time = generate_random_timestamp().timestamp()
    drop_off_location = generate_random_location()
    return {
      "pickup_location": pickup_location,
      "pickup_time": pickup_time,
      "drop_off_location": drop_off_location
    }


def generate_driver_data_point():
    current_location = generate_random_location()
    driver_price = random.randint(MIN_DRIVER_PRICE, MAX_DRIVER_PRICE)
    return {
        "driver_price": driver_price,
        "current_location": current_location,
        "next_availability": START_TIME.timestamp()
    }


rides = []
drivers = []

for i in range(100):
    rides.append(Ride(**generate_ride_data_point()))

for i in range(100):
    drivers.append(Driver(**generate_driver_data_point()))


ride_manager = RideManager(date="2024-05-26")
rides = ride_manager.sort_rides(rides)
ride_manager.assign_rides_to_drivers(rides, drivers)
print(f"{ride_manager.rides_driver_mapping = }")
print(f"{len(ride_manager.rides_driver_mapping) = }")
