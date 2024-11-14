from turfpy.random import random_position
from turfpy.measurement import destination
from geojson import Point
import json
import random


class Unit:
    def __init__(self, unit_name, bound, speed=0, course=0,latitude=None, longitude=None):
        self.unit_name = unit_name
        # self.latitude, self.longitude = self.generate_random_location(bound)
        self.speed = speed  # in knots
        self.course = course  # in degrees

        # If latitude and longitude are provided, use them; otherwise, generate random location
        if latitude is not None and longitude is not None:
            self.latitude = latitude
            self.longitude = longitude
        else:
            self.latitude, self.longitude = self.generate_random_location(bound)

    @staticmethod
    def generate_random_location(bound):
        # Generate a random location within the given latitude and longitude bounds
        coordinates = random_position(bound)
        return coordinates[1], coordinates[0]  # Return as (latitude, longitude)

    def update_position(self, time_interval):
        # Calculate new position based on speed and course over time
        distance = (self.speed * time_interval) / 3600  # time interval in seconds
        start_point = Point((self.longitude, self.latitude))
        new_location = destination(start_point, distance, self.course)
        new_coordinates = new_location["geometry"]["coordinates"]
        self.latitude, self.longitude = new_coordinates[1], new_coordinates[0]

    def __str__(self):
        return (f"{self.unit_name} - Position:(Lat{self.latitude:.6f},Long {self.longitude:.6f}), "
                f"Speed: {self.speed} knots, Course: {self.course}°")


# Subclass for Aircraft
class Aircraft(Unit):
    def __init__(self, bound, speed=0, course=0, height=0, subtype="",latitude=None, longitude=None):
        super().__init__("Aircraft", bound, speed, course, latitude, longitude)
        self.height = height  # altitude in meters
        self.subtype = subtype

    def __str__(self):
        return (f"{self.unit_name} ({self.subtype}) - Position: (Lat{self.latitude:.6f},Long {self.longitude:.6f}), "
                f"Speed: {self.speed} knots, Course: {self.course}°, Height: {self.height} m")


# Subclass for Ship
class Ship(Unit):
    def __init__(self, bound, speed=0, course=0, subtype="",latitude=None, longitude=None):
        super().__init__("Ship", bound, speed, course, latitude, longitude)
        self.subtype = subtype

    def __str__(self):
        return (f"{self.unit_name} ({self.subtype}) - Position: (Lat{self.latitude:.6f},Long {self.longitude:.6f}), "
                f"Speed: {self.speed} knots, Course: {self.course}°")


# Subclass for Submarine
class Submarine(Unit):
    def __init__(self, bound, speed=0, course=0, depth=0, subtype="",latitude=None, longitude=None):
        super().__init__("Submarine", bound, speed, course, latitude, longitude)
        self.depth = depth  # depth in meters
        self.subtype = subtype

    def __str__(self):
        return (f"{self.unit_name} ({self.subtype}) - Position: (Lat{self.latitude:.6f},Long {self.longitude:.6f}), "
                f"Speed: {self.speed} knots, Course: {self.course}°, Depth: {self.depth} m")

#Subclass for Base
class Base(Unit):
    def __init__(self, bound, subtype="", latitude=None, longitude=None):
        super().__init__("Base", bound, latitude, longitude)
        self.subtype = subtype 

    def __str__(self):
        return (f"{self.unit_name} ({self.subtype}) - Position: (Lat{self.latitude:.6f},Long {self.longitude:.6f})") 

# Example bounds for generating random positions
#[bbox=[min_longitude, min_latitude, max_longitude, max_latitude]]
min_longitude,min_latitude, max_longitude, max_latitude = 68,8,97.2,37.5
bound = [min_longitude,min_latitude, max_longitude, max_latitude]


# Load the unit-subtype data from the JSON file
def load_unit_subtypes(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Get a random unit-subtype for the given unit type
def get_random_unit_subtype(unit_type, unit_subtypes):
    if unit_type in unit_subtypes:
        return random.choice(unit_subtypes[unit_type])
    else:
        return None  # If unit type is not found

# Example usage
unit_subtypes = load_unit_subtypes('unit_subtypes.json')

# Create instances of each unit type
aircraft = Aircraft(bound, speed=500, course=90, height=10000, subtype=get_random_unit_subtype('Aircraft', unit_subtypes))
aircraft2 = Aircraft(bound, speed=800, course=10, height=10000, subtype=get_random_unit_subtype('Aircraft', unit_subtypes))
aircraft3 = Aircraft(bound, speed=200, course=180, height=10000, subtype=get_random_unit_subtype('Aircraft', unit_subtypes))
ship = Ship(bound, speed=20, course=45, subtype=get_random_unit_subtype('Ship', unit_subtypes))
ship2 = Ship(bound, speed=10, course=5, subtype=get_random_unit_subtype('Ship', unit_subtypes))
ship3 = Ship(bound, speed=40, course=0, subtype=get_random_unit_subtype('Ship', unit_subtypes))
submarine = Submarine(bound, speed=15, course=135, depth=200, subtype=get_random_unit_subtype('Submarine', unit_subtypes))
submarine2 = Submarine(bound, speed=10, course=13, depth=100, subtype=get_random_unit_subtype('Submarine', unit_subtypes))
submarine3 = Submarine(bound, speed=5, course=135, depth=20, subtype=get_random_unit_subtype('Submarine', unit_subtypes))
base = Base(bound, subtype=get_random_unit_subtype('Base', unit_subtypes))

# Print initial positions
print("Initial Positions:")
print(aircraft)
print(aircraft2)
print(aircraft3)
print(ship)
print(ship2)
print(ship3)
print(submarine)
print(submarine2)
print(submarine3)
print(base)

# Define the interval and total duration
interval = 600  # 10 minutes in seconds
total_time = 3600  # 1 hour in seconds


print("\nPositions at each 10-minute interval:")
for elapsed_time in range(interval, total_time + interval, interval):
    print(f"\nAfter {elapsed_time // 60} minutes:")
    aircraft.update_position(interval)
    aircraft2.update_position(interval)
    aircraft3.update_position(interval)
    ship.update_position(interval)
    ship2.update_position(interval)
    ship3.update_position(interval)
    submarine.update_position(interval)
    submarine2.update_position(interval)
    submarine3.update_position(interval)

    # Print updated positions
    print(aircraft)
    print(aircraft2)
    print(aircraft3)
    print(ship)
    print(ship2)
    print(ship3)
    print(submarine)
    print(submarine2)
    print(submarine3)





