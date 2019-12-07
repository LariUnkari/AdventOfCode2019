"""Advent of Code 2019 - Day 6"""

class Body:
    """Defines a body that can be orbited, it's orbit to the parent body
    and any satellite orbits from other bodies
    """
    def __init__(self, name, orbit, satellite_orbits):
        self.name = name
        self.orbit = orbit
        self.satellite_orbits = satellite_orbits

    def set_parent(self, parent_body):
        self.orbit = Orbit(parent_body, self)

    def add_satellite(self, satellite_body):
        self.satellite_orbits.append(Orbit(self, satellite_body))

    def count_orbit_links_to_com(self, number, log_level):
        """Calculates orbits through parent bodies all the way to COM"""

        if self.orbit != None and self.orbit.parent != None:
            number += 1
            if log_level >= 3:
                print(f"{self.name} orbits {self.orbit.parent.name}. Orbit count now {number}")
            return self.orbit.parent.count_orbit_links_to_com(number, log_level)

        return number

class Orbit:
    """Defines an orbit between two bodies"""
    
    def __init__(self, parent, satellite):
        self.parent = parent
        self.satellite = satellite


COM_NAME = "COM"


def play(input_parameter, log_level):


    #Initialize and read input


    input_file = open("data/day6input.txt", "r")
    input_strings = [line.strip() for line in input_file.readlines()]

    orbit_char_index = 0
    name_a, name_b = "", ""
    body_parent, body_satellite = None, None
    body_map = {}

    for i in input_strings:
        orbit_char_index = i.index(")")
        name_a = i[0:orbit_char_index]
        name_b = i[orbit_char_index+1:]

        if log_level >= 3:
            print(f"Orbit info: {i}, {name_b} is a satellite of {name_a}")

        if name_a in body_map:
            body_parent = body_map[name_a]
            if log_level >= 3:
                print(f"Found body {name_a} in map")
        else:
            body_parent = Body(name_a, None, [])
            body_map[name_a] = body_parent
            if log_level >= 2:
                print(f"Added body {name_a} into map")

        if name_b in body_map:
            body_satellite = body_map[name_b]
            if body_satellite.orbit != None:
                parent_name = body_satellite.orbit.parent.name if body_satellite.orbit.parent != null else "None"
                print(f"ERROR: Known body {name_b} orbiting {parent_name} was found again as satellite of {name_a}!")
                continue
            if log_level >= 3:
                print(f"Found body {name_b} in map")
        else:
            body_satellite = Body(name_b, None, [])
            body_map[name_b] = body_satellite
            if log_level >= 2:
                print(f"Added body {name_b} into map")

        body_satellite.set_parent(body_parent)
        body_parent.add_satellite(body_satellite)

        if log_level >= 3:
            child_count = len(body_parent.satellite_orbits)
            print(f"Set body {name_b} as satellite of {name_a}, satellite count now {child_count}")

    com = None
    if COM_NAME in body_map:
        com = body_map[COM_NAME]
        if log_level >= 1:
            child_count = len(com.satellite_orbits)
            print(f"Found root {COM_NAME}, child count is {child_count}")
    else:
        print(f"ERROR: No root {COM_NAME} found!")
        return


    #Run the program


    #Part 1 of Day 6

    
    #Count universal center of mass by iterating through bodies
    orbit_count = 0

    for name in body_map:
        body = body_map[name]

        if body.orbit != None:
            if body.orbit.parent != None:
                orbit_count = body.count_orbit_links_to_com(orbit_count, log_level)
            else:
                print(f"ERROR! Body {body.name} orbits nothing!") #This should never happen
        elif log_level >= 1:
            print(f"Body {body.name} has no orbit!") #COM is like this, but others shouldn't be

    print(f"Final orbit count is {orbit_count}")
