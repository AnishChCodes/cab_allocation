class RideManager:
    def __init__(self, date):
        self.date = date
        self.rides_driver_mapping = []

    @staticmethod
    def sort_rides(rides):
        rides.sort(key=lambda ride: ride.pickup_time)
        return rides

    def find_and_assign_driver(self, ride, driver_list):
        driver_pickup_cost = None
        ride_cost = None
        assigned_driver = None

        for driver in driver_list:
            if driver.driver_available(ride.pickup_location, ride.pickup_time):
                temp_driver_pickup_cost, temp_ride_cost = (int(driver.calculate_pickup_cost(ride.pickup_location)),
                                                           int(ride.displacement * driver.driver_price))
                if not assigned_driver:
                    driver_pickup_cost, ride_cost = temp_driver_pickup_cost, temp_ride_cost
                    assigned_driver = driver
                elif temp_driver_pickup_cost <= driver_pickup_cost and temp_ride_cost <= ride_cost:
                    driver_pickup_cost = temp_driver_pickup_cost
                    ride_cost = temp_ride_cost
                    assigned_driver = driver

        if assigned_driver:
            ride.assign_driver(assigned_driver)
            assigned_driver.assign_ride(ride)
            assigned_driver.expected_next_availability = ride.drop_off_time
            assigned_driver.expected_next_location = ride.drop_off_location
            self.rides_driver_mapping.append({
                "driver": assigned_driver,
                "ride": ride
            })

    def assign_rides_to_drivers(self, ride_list, driver_list):
        for ride in ride_list:
            self.find_and_assign_driver(ride, driver_list)
