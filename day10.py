"""Advent of Code 2019 - Day 9"""
from fractions import Fraction


#Global definitions


def find_best_site(map_data, width, height, log_level):
    """Scans from each coordinate in map data and finds the one with highest amount of visible asteroids.
    Returns a tuple with asteroid count and coordinate tuple (count, (x, y))
    """

    count = 0
    highest_count = 0
    best_coordinate = (-1, -1)
    
    for coordinate in map_data:
        if log_level >= 1:
            print(f"Scanning from {coordinate}")

        count = scan_from_position(map_data, coordinate, width, height, log_level)

        if log_level >= 1:
            print(f"{count} asteroids visible from {coordinate}")

        if count > highest_count:
            highest_count = count
            best_coordinate = coordinate

    return (highest_count, best_coordinate)

def scan_from_position(map_data, position, width, height, log_level):
    """Scans view of asteroids from given position and map data parameters.
    Returns the count of asteroids found.
    """
    
    count = 0
    visibility_map = map_data.copy()

    for coordinate in map_data:
        if coordinate[0] == position[0] and coordinate[1] == position[1]:
            if log_level >= 2:
                print(f"Skipping asteroid at {coordinate} due to being the same as scan position.")

            continue

        step = get_smallest_step(coordinate, position)

        if log_level >= 2:
            print(f"Smallest step on line from {position} to {coordinate} is {step}")

        x = position[0]
        y = position[1]

        #Find each asteroid in steps from position towards coordinate (and beyond if applicable)
        isObstructed = False

        while True:
            x += step[0]
            y += step[1]

            if x < 0 or x >= width or y < 0 or y >= height:
                if log_level >= 3:
                    print(f"Out of bounds: {x},{y} from {position} towards {coordinate}")

                break

            if log_level >= 3:
                print(f"Step to {x},{y} from {position} towards {coordinate}")

            if (x, y) in visibility_map:
                if not isObstructed:
                    isObstructed = True #Everything along the line past first contact is obstructed

                    if visibility_map[(x, y)] == 0:
                        visibility_map[(x, y)] = 1
                        count += 1

                        if log_level >= 1:
                            print(f"Asteroid visible at {x},{y} from {position}, count at {count}")
                    else:
                        if visibility_map[(x, y)] == 1:
                            if log_level >= 2:
                                print(f"Asteroid already visible at {x},{y} from {position}, not counted in")
                        else:
                            if log_level >= 2:
                                print(f"Asteroid obstructed at {x},{y} from {position}, not counted in")
                else:
                    if visibility_map[(x, y)] >= 0:
                        if visibility_map[(x, y)] == 1:
                            count -= 1 #Reduce visible count
                            if log_level >= 1:
                                print(f"Asteroid obstructed at {x},{y} from {position} and no longer visible, count at {count}")
                        else:
                            if log_level >= 1:
                                print(f"Asteroid obstructed at {x},{y} from {position} and no longer viable for visibility")
                    else:
                        if log_level >= 2:
                            print(f"Asteroid obstructed at {x},{y} from {position}, not counted in")
                        
                    visibility_map[(x, y)] = -1

    return count

def get_smallest_step(coordinate, position):
    """Finds the smallest step on a line from position to coordinate.
    Returns a tuple (int, int).
    """
    
    #Straight lines are simple
    if coordinate[0] == position[0]:
        return (0, 1 if coordinate[1] > position[1] else -1) #Straight line along y axis, no x movement
    elif coordinate[1] == position[1]:
        return (1 if coordinate[0] > position[0] else -1, 0) #Straight line along x axis, no y movement

    #Angled line, use Fraction class to reduce to smallest grid-aligned step possible
    fraction = Fraction(coordinate[0] - position[0], coordinate[1] - position[1])

    #Fraction reduces away any negative denominator, this fixes it by
    #inverting both if the denominator is supposed to be a negative value
    if coordinate[1] < position[1]:
        return (-fraction.numerator, -fraction.denominator)
    
    return (fraction.numerator, fraction.denominator)

#Program
    

def play(input_file, input_parameters, log_level):
    """Program entry point"""


    #Initialize and read input


    #Parse map data
    map_data = []
    width, height = 0, 0

    y = 0
    for line in input_file:
        map_data.append(line.strip())

        if width == 0: 
            width = len(map_data[y])

        if log_level >= 1:
            print(f"Row {y:02d} of input data: {map_data[y]}")

        y += 1

    height = y

    if log_level >= 1:
        print(f"Map data dimensions: {width}x{height}")

    #Map all asteroids
    map_asteroids = {}
    
    x = 0
    y = 0
    for row in map_data:
        for c in row:

            if c == '#':
                map_asteroids[(x, y)] = 0

                if log_level >= 2:
                    print(f"Asteroid found at {x},{y}")
            else:
                if log_level >= 2:
                    print(f"Clear space found at {x},{y}")

            x += 1

        x = 0
        y += 1


    #Run the program


    result = find_best_site(map_asteroids, width, height, log_level)
    print(f"Best site: {result[0]} asteroids visible to {result[1][0]},{result[1][1]}")