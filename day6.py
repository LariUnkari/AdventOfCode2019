"""Advent of Code 2019 - Day 6"""


#Global definitions


COM_NAME = "COM"

class Body:
    """Defines a body that can be orbited, it's orbit to the parent body
    and any satellite orbits from other bodies
    """
    def __init__(self, name, orbit, satellite_orbits):
        self.name = name
        self.orbit = orbit
        self.satellite_orbits = satellite_orbits

    def set_parent(self, parent_body):
        self.orbit.parent = parent_body

    def add_satellite(self, orbit):
        self.satellite_orbits.append(orbit)

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
    
    def __init__(self, name, parent, satellite):
        self.name = name
        self.parent = parent
        self.satellite = satellite

def init_map(input_strings, log_level):
    """Walks through input strings and builds a map out of it"""

    #Process all orbits into a map and add all orbit links to each body to which they belong
    orbit_char_index = 0
    name_a, name_b = "", ""
    orbit = None
    body_parent, body_satellite = None, None
    body_map = {}

    for i in input_strings:
        orbit_char_index = i.index(")")
        name_a = i[0:orbit_char_index]
        name_b = i[orbit_char_index+1:]

        orbit = Orbit(i, None, None)

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
                parent_name = body_satellite.orbit.parent.name if body_satellite.orbit.parent != None else "None"
                print(f"ERROR: Known body {name_b} orbiting {parent_name} was found again as satellite of {name_a}!")
                continue
            if log_level >= 3:
                print(f"Found body {name_b} in map")
        else:
            body_satellite = Body(name_b, orbit, [])
            body_map[name_b] = body_satellite
            if log_level >= 2:
                print(f"Added body {name_b} into map")

        #Update orbit and bodies
        orbit.parent = body_parent
        orbit.satellite = body_satellite
        body_parent.add_satellite(orbit)
        body_satellite.orbit = orbit

        if log_level >= 3:
            child_count = len(body_parent.satellite_orbits)
            print(f"Set body {name_b} as satellite of {name_a}, satellite count now {child_count}")

    return body_map


#Part 1 of Day 6


def part_1(body_map, log_level):
    """Solution to part 1"""

    #Find universal center of mass
    com = None
    if COM_NAME in body_map:
        com = body_map[COM_NAME]
        if log_level >= 1:
            child_count = len(com.satellite_orbits)
            print(f"Found root {COM_NAME}, child count is {child_count}")
    else:
        print(f"ERROR: No root {COM_NAME} found!")
        return

    #Count links to universal center of mass by iterating through bodies
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

    print(f"Total orbit link count is {orbit_count}")


#Part 2 of Day 6


def part_2(body_map, start_body_name, target_body_name, log_level):
    """Solution to part 2"""

    #Find start and target bodies
    start_body = None
    target_body = None

    if start_body_name in body_map:
        my_body = body_map[start_body_name]
        if my_body.orbit != None and my_body.orbit.parent != None:
            start_body = my_body.orbit.parent

    if target_body_name in body_map:
        santa_body = body_map[target_body_name]
        if my_body.orbit != None and santa_body.orbit.parent != None:
            target_body = santa_body.orbit.parent

    if start_body == None or target_body == None:
        print(f"Error finding start {start_body_name} and target {target_body_name} bodies")
        return
    
    #Starting from body orbited by start body, use fill-search to find target
    #Links are tuples of (next Body, via Orbit, from Orbit)
    closed_map = {} #Links already processed
    next_link = seek_target((start_body, my_body.orbit, None), target_body, closed_map, log_level)

    #Walk back via links to form a path
    orbit_transfer_links = [next_link]
    
    via_orbit = next_link[1]
    next_orbit = next_link[2]

    while next_orbit.parent != my_body and next_orbit.satellite != my_body:
        orbit_transfer_links.append(next_link)

        if log_level >= 2:
            print(f"Walking back... from {via_orbit.name} via {next_orbit.name}")

        next_link = closed_map[next_orbit.name]
        via_orbit = next_link[1]
        next_orbit = next_link[2]

    print(f"Total orbit transfer count is {len(orbit_transfer_links)}")

def seek_target(start_link, target_body, closed_map, log_level):
    """Walks through orbit links and immediately returns the link
    to target body if found, or None if never found
    """
    open_list = [start_link] #Orbit links to check
    body_to, orbit_to = None, None

    for link in open_list:
        body_to = link[0]
        orbit_to = link[1]

        if log_level >= 2:
            print(f"Visiting body {body_to.name} via orbit {orbit_to.name}")

        closed_map[orbit_to.name] = link #Mark link as processed under orbit name

        new_links = visit_link(link, closed_map, log_level)
        for l in new_links:
            body_to = l[0]
            orbit_to = l[1]
            if body_to == target_body:
                if log_level >= 1:
                    print(f"Found target body {target_body.name} via orbit {orbit_to.name}!")
                closed_map[orbit_to.name] = l
                return l
            
        #This looks so horrible, modifying a list in a loop, but it works!
        open_list.extend(new_links)

    return None

def visit_link(link, closed_map, log_level):
    """Adds any new orbit links from visited link to open list.
    Returns list of new links to visit
    """
    new_links = []
    visited_body = link[0]
    via_orbit = link[1]
    from_orbit = link[2]

    #Parent
    if visited_body.orbit != None:
        if visited_body.orbit != from_orbit:
            if not visited_body.orbit.name in closed_map:
                if log_level >= 2:
                    print(f"Adding {visited_body.name} parent orbit link {visited_body.orbit.name} to list")
                new_links.append((visited_body.orbit.parent, visited_body.orbit, via_orbit))
            elif log_level >= 2:
                print(f"{visited_body.orbit.name} satellite orbit link already visited")
        elif log_level >= 2:
            print(f"{visited_body.orbit.name} parent orbit was source of this visit")

    #Satellites
    for satellite_orbit in visited_body.satellite_orbits:
        if satellite_orbit != from_orbit:
            if not satellite_orbit.name in closed_map:
                if log_level >= 2:
                    print(f"Adding {visited_body.name} satellite orbit link {satellite_orbit.name} to list")
                new_links.append((satellite_orbit.satellite, satellite_orbit, via_orbit))
            elif log_level >= 2:
                print(f"{satellite_orbit.name} satellite orbit link already visited")
        elif log_level >= 2:
            print(f"{satellite_orbit.name} satellite orbit was source of this visit")

    return new_links


#Program

    
def play(input_parameters, log_level):
    """Program entry point"""


    #Initialize and read input


    input_file = open("data/day6input.txt", "r")
    input_strings = [line.strip() for line in input_file.readlines()]
    
    body_map = init_map(input_strings, log_level)


    #Run the program


    output = 0
    txt = input("Choose part 1 or 2 (defaults to 2): ")
    if txt == "1":
        part_1(body_map, log_level)
    else:
        part_2(body_map, "YOU", "SAN", log_level)
    
