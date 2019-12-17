"""Advent of Code 2019 - Day 9"""
from fractions import Fraction


#Global definitions


CHAR_ASTEROID = '#'
CHAR_STATION = 'X'

def create_asteroid_data(map_data, default_value, log_level):
    """Maps all asteroids into a dictionary with coordinate tuple as key and integer as value.
    Returns a tuple (count, dictionary).
    """
    count = 0
    map_asteroids = {}
    
    x = 0
    y = 0
    for row in map_data:
        for c in row:

            if c == CHAR_ASTEROID:
                map_asteroids[(x, y)] = default_value
                count += 1

                if log_level >= 2:
                    print(f"Asteroid found at {x},{y}")
            else:
                if log_level >= 2:
                    print(f"Clear space found at {x},{y}")

            x += 1

        x = 0
        y += 1

    return (count, map_asteroids)

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

def find_station(map_data, log_level):
    """Seeks station char in the map data and returns it's position."""
    
    x,y = 0,0
    for row in map_data:
        for c in row:
            if c == CHAR_STATION:
                return (x,y)

            x += 1

        x = 0
        y += 1
                
    return (-1,-1)


#Part 1 of Day 10


def part_1(map_data, width, height, log_level):
    """Slightly optimized to only check locations of known asteroids."""
    
    asteroid_data = create_asteroid_data(map_data, 0, log_level)
    result = find_best_site(asteroid_data[1], width, height, log_level)
    print(f"Best site: {result[0]} asteroids visible to {result[1][0]},{result[1][1]}")

    return result[1]
    
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

        if log_level >= 2:
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
            if log_level >= 3:
                print(f"Skipping asteroid at {coordinate} due to being the same as scan position.")

            continue

        step = get_smallest_step(coordinate, position)

        if log_level >= 3:
            print(f"Smallest step on line from {position} to {coordinate} is {step}")

        x = position[0]
        y = position[1]

        #Find each asteroid in steps from position towards coordinate (and beyond if applicable)
        isObstructed = False

        while True:
            x += step[0]
            y += step[1]

            if x < 0 or x >= width or y < 0 or y >= height:
                if log_level >= 4:
                    print(f"Out of bounds: {x},{y} from {position} towards {coordinate}")

                break

            if log_level >= 4:
                print(f"Step to {x},{y} from {position} towards {coordinate}")

            if (x, y) in visibility_map:
                if not isObstructed:
                    isObstructed = True #Everything along the line past first contact is obstructed

                    if visibility_map[(x, y)] == 0:
                        visibility_map[(x, y)] = 1
                        count += 1

                        if log_level >= 2:
                            print(f"Asteroid visible at {x},{y} from {position}, count at {count}")
                    else:
                        if visibility_map[(x, y)] == 1:
                            if log_level >= 3:
                                print(f"Asteroid already visible at {x},{y} from {position}, not counted in")
                        else:
                            if log_level >= 3:
                                print(f"Asteroid obstructed at {x},{y} from {position}, not counted in")
                else:
                    if visibility_map[(x, y)] >= 0:
                        if visibility_map[(x, y)] == 1:
                            count -= 1 #Reduce visible count
                            if log_level >= 2:
                                print(f"Asteroid obstructed at {x},{y} from {position} and no longer visible, count at {count}")
                        else:
                            if log_level >= 2:
                                print(f"Asteroid obstructed at {x},{y} from {position} and no longer viable for visibility")
                    else:
                        if log_level >= 3:
                            print(f"Asteroid obstructed at {x},{y} from {position}, not counted in")
                        
                    visibility_map[(x, y)] = -1

    return count


#Part 2 of Day 10


def part_2(map_data, position, width, height, log_level):
    """Divides the map data into 8 segments, starting from top orthogonal towards top-right diagonal.
    Rotates a laser and keeps rotating after each first scan hit, destroying asteroids as it goes.
    """

    asteroid_data = create_asteroid_data(map_data, -1, log_level)
    asteroid_count = asteroid_data[0]
    asteroid_map = asteroid_data[1]

    #Remove station position from data
    del asteroid_map[position]
    asteroid_count -= 1

    print(f"Sweeping with laser from {position} to destroy {asteroid_count} asteroids in total.")
    
    asteroids_remaining = asteroid_count
    list_asteroids_destroyed = []
    asteroids_destroyed = 0
    pass_number = 1

    while asteroids_remaining > 0:
        for i in range(8):
            new_hits = sweep_segment(asteroid_map, width, height, position, i, log_level)
            asteroids_destroyed += len(new_hits)
            list_asteroids_destroyed.extend(new_hits)

        print(f"{asteroids_destroyed} asteroids destroyed in pass {pass_number}")

        if log_level >= 1:
            index = 0
            coordinate = 0
            for n in range(asteroid_count - asteroids_remaining, len(list_asteroids_destroyed)):
                index = n + 1
                coordinate = list_asteroids_destroyed[n]
                print(f"{index:003d}: Hit {coordinate} in segment {asteroid_map[coordinate]}")
            
        asteroids_remaining -= asteroids_destroyed

        print(f"{asteroids_remaining} asteroids remain after pass {pass_number}")
        asteroids_destroyed = 0
        pass_number += 1

    #Give user input choice over asteroid info for answer

    txt = input(f"Get coordinate of destroyed asteroid at place (1-{len(list_asteroids_destroyed)}): ")

    if len(txt) < 1:
        print(f"Empty number input")
        return

    asteroid_number = 0
    try:
        asteroid_number = int(txt)
    except ValueError:
        print(f"Invalid number input {txt}")
        return

    if asteroid_number > 0 and asteroid_number <= len(list_asteroids_destroyed):
        asteroid_position = list_asteroids_destroyed[asteroid_number - 1]
        answer = asteroid_position[0] * 100 + asteroid_position[1]
        print(f"Asteroid number {asteroid_number} was hit at {asteroid_position}")
        print(f"Answer to 100 * {asteroid_position[0]} + {asteroid_position[1]} is {answer}")
    else:
        print(f"Number input {asteroid_number} out of bounds!")

def sweep_segment(asteroid_map, width, height, position, segment_index, log_level):
    """One by one scans the segment in a clockwise scanline rotation from position.
    Returns list of asteroids hit.
    """
    if log_level >= 2:
        print(f"Segment {segment_index}: starting sweep scan from {position}")

    list_asteroids_destroyed = []
    is_inverse = segment_index % 2 == 1

    #Map the segment space into map space with step and dimension conversions
    up_step = (0,-1)
    side_step = (1,0)
    scan_width = width - position[0]
    scan_height = position[1]
    if segment_index == 1:
        up_step = (1,0)
        side_step = (0,-1)
        scan_width = position[1]
        scan_height = width - position[0]
    elif segment_index == 2:
        up_step = (1,0)
        side_step = (0,1)
        scan_width = height - position[1]
        scan_height = width - position[0]
    elif segment_index == 3:
        up_step = (0,1)
        side_step = (1,0)
        scan_width = width - position[0]
        scan_height = height - position[1]
    elif segment_index == 4:
        up_step = (0,1)
        side_step = (-1,0)
        scan_width = position[0]
        scan_height = height - position[1]
    elif segment_index == 5:
        up_step = (-1,0)
        side_step = (0,1)
        scan_width = height - position[1]
        scan_height = position[0]
    elif segment_index == 6:
        up_step = (-1,0)
        side_step = (0,-1)
        scan_width = position[1]
        scan_height = position[0]
    elif segment_index == 7:
        up_step = (0,-1)
        side_step = (-1,0)
        scan_width = position[0]
        scan_height = position[1]

    #Saves a bit to constrain width to height
    if scan_width > scan_height:
        scan_width = scan_height

    steps_list = get_all_steps_in_segment(segment_index, scan_width, scan_height, log_level)

    if log_level >= 2:
        print(f"Found {len(steps_list)} steps to scan")

    if is_inverse:
        if log_level >= 2:
            print(f"Reversing list in inverted segment {segment_index}")
        steps_list.reverse()

    if log_level >= 2:
        print(f"Step list: {steps_list}")

    x,y,i = 0,0,1
    for step in steps_list:
        if log_level >= 3:
            print(f"Scanning from {position}, step {step} in segment {segment_index}")

        while True:
            x = position[0] + i * (step[0] * side_step[0] + step[1] * up_step[0])
            y = position[1] + i * (step[0] * side_step[1] + step[1] * up_step[1])

            if x < 0 or x >= width or y < 0 or y >= height:
                if log_level >= 4:
                    print(f"Stopping step scan at position {x},{y} (step {i}) due to out of bounds {width},{height}")
                break
        
            if log_level >= 4:
                print(f"Scanning position {x},{y} (step {i})")

            #Destroy asteroid if found
            if (x,y) in asteroid_map and asteroid_map[(x,y)] < 0:
                asteroid_map[(x,y)] = segment_index
                list_asteroids_destroyed.append((x,y))
                if log_level >= 4:
                    print(f"Stopping step scan at position {x},{y} (step {i}) due to asteroid hit")
                break

            i += 1

        i = 1

    return list_asteroids_destroyed

def get_all_steps_in_segment(segment_index, width, height, log_level):
    """Finds all possible unique angles for laser in a segment.
    Returns a list of step tuples (x,y)
    """
    if log_level >= 2:
        print(f"Gettings steps to scan for segment {segment_index}, height={height}, width={width}")

    steps_dict = {}
    steps_list = []

    if segment_index % 2 == 0:
        step = (0,1)
        steps_list.append(step)

        if log_level >= 3:
            print(f"Segment {segment_index}: added orthogonal segment step {step} to the beginning of list")

    #From top and one to the side, get all unique steps in segment
    x = 1
    y = height

    while True:
        step = get_smallest_step((x,y), (0,0)) #Reduce the step to smallest components

        #If this step was not yet found, add it
        if not step in steps_dict:
            steps_dict[step] = True
            steps_list.append(step)

            if log_level >= 3:
                print(f"Segment {segment_index}: added segment step {step}")
            
        #Move down the segment, or go the next column if y would meet x (diagonal)
        if y - 1 <= x:
            y = height
            x += 1

            if log_level >= 4:
                print(f"Segment {segment_index}: moved to new column, segment position {x},{y}")
        else:
            y -= 1

            if log_level >= 4:
                print(f"Segment {segment_index}: moved to segment position {x},{y}")

        #Stop if at the end
        if x > width or y > height:
            if log_level >= 4:
                print(f"Segment {segment_index}: {x},{y} out of bounds")

            break
        elif x == y:
            if log_level >= 4:
                print(f"Segment {segment_index}: {x},{y} at diagonal end")

            break

    if segment_index % 2 == 1:
        step = (1,1)
        steps_list.append(step)

        if log_level >= 3:
            print(f"Segment {segment_index}: added diagonal segment step {step} to the end of list")
                
    if log_level >= 4:
        print(f"Segment {segment_index}: Sorting list")

    steps_list.sort(key=lambda elem: elem[0] / elem[1])

    return steps_list


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

    
    #Run the program
    

    position = (0,0)

    txt = input("Choose part 1 or 2 (other inputs run both in sequence): ")
    if txt == "2":
        #Used for debugging part 2 with test data
        position = find_station(map_data, log_level)

        if position[0] < 0 or position[1] < 0:
            print("No viable station {station_char} location found in map data!")
            return
    else:
        position = part_1(map_data, width, height, log_level)

        #If only part 1 chosen, exit now
        if txt == "1":
            return

    part_2(map_data, position, width, height, log_level)