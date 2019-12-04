"""Advent of Code 2019 - Day 3"""

class Coordinate:
    """An object that represents a 2D-position on a grid"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)

    def copy(self):
        return Coordinate(self.x, self.y)

    def to_string(self):
        return COORDINATE_STRING_FORMAT.format(self.x, self.y)

class LineInstruction:
    """An object that contains the necessary information to form a line out of"""

    def __init__(self, line_index, direction, length):
        self.line_index = line_index
        self.direction = direction
        self.length = length
        if LOG_LEVEL >= 2:
            print("[{0}]LineInstruction(dir={1}, len={2})".format(line_index, direction, length))

    def walk(self, map_data, coordinate, action, *args):
        """Runs through line instructions and marks each passed coordinate down.
        Alternatively checks if a crossing was found and marks that up
        """
        if self.direction == "U":
            for i in range(self.length):
                coordinate.y += 1
                if LOG_LEVEL >= 2:
                    print("Moved up {0}/{1} to {2}".format(i, self.length, coordinate.to_string()))
                action(map_data, coordinate, *args)
        elif self.direction == "R":
            for i in range(self.length):
                coordinate.x += 1
                if LOG_LEVEL >= 2:
                    print("Moved right {0}/{1} to {2}".format(i, self.length, coordinate.to_string()))
                action(map_data, coordinate, *args)
        elif self.direction == "D":
            for i in range(self.length):
                coordinate.y -= 1
                if LOG_LEVEL >= 2:
                    print("Moved down {0}/{1} to {2}".format(i, self.length, coordinate.to_string()))
                action(map_data, coordinate, *args)
        elif self.direction == "L":
            for i in range(self.length):
                coordinate.x -= 1
                if LOG_LEVEL >= 2:
                    print("Moved left {0}/{1} to {2}".format(i, self.length, coordinate.to_string()))
                action(map_data, coordinate, *args)

        return coordinate


#Initialize and read input


LOG_LEVEL = 1

COORDINATE_STRING_FORMAT = "{0},{1}"

LINES = []
LINE_MAP = {}
LINE_CROSSINGS = []

INPUT_FILE = open("input.txt", "r")
INPUT_STRINGS = [INPUT_FILE.readline().split(","), INPUT_FILE.readline().split(",")]

#Iterate with index to save index on line instructions
for index in range(len(INPUT_STRINGS)):
    line = []

    for line_input in INPUT_STRINGS[index]:
        line.append(LineInstruction(index, line_input[0], int(line_input[1:])))

    LINES.append(line)


#Part 1 of Day 3


def set_line_at_coordinate(map_data, coordinate, *args):
    """Marks down that a line passes over a coordinate."""
    map_data[coordinate.to_string()] = True

def check_crossing_at_coordinate(map_data, coordinate, *args):
    """Checks if a line already passed over a given coordinate."""
    cs = coordinate.to_string()
    if cs in map_data:
        if LOG_LEVEL >= 1:
            print("Coordinate {0} exists in map!".format(cs))
        if map_data[cs]:
            LINE_CROSSINGS.append(coordinate.copy())
            if LOG_LEVEL >= 1:
                print("Lines cross at {0}".format(cs))

def walk_lines(map_data, line_a, line_b):
    """Draw lines on map and marks crossings"""

    #Draw the line on map, then register crossing on second line
    #No need to register starting point crossings
    coordinate = Coordinate(0,0)
    for instruction in line_a:
        coordinate = instruction.walk(map_data, coordinate, set_line_at_coordinate)

    coordinate = Coordinate(0,0)
    for instruction in line_b:
        coordinate = instruction.walk(map_data, coordinate, check_crossing_at_coordinate)

def find_nearest_crossing_manhattan(line_crossings):
    """Seeks the closest line crossing in manhattan distance to origo"""

    shortest_manhattan_distance = -1
    nearest_crossing_coordinate = None
    distance = 0

    for crossing in line_crossings:
        distance = crossing.manhattan_distance()

        #Disregard starting position
        if distance <= 0:
            continue

        #Check if closer
        if shortest_manhattan_distance < 0 or distance < shortest_manhattan_distance:
            shortest_manhattan_distance = distance
            nearest_crossing_coordinate = crossing
            if LOG_LEVEL >= 1:
                print("New nearest crossing candidate found at {0}, distance {1}".format(
                    crossing.to_string(), distance))

    #Finish and return the answer with coordinate and distance
    if shortest_manhattan_distance > 0:
        return (nearest_crossing_coordinate, shortest_manhattan_distance)

    #Nothing found
    return (None, -1)


#Walk the lines
walk_lines(LINE_MAP, LINES[0], LINES[1])

#Find the nearest in manhattan distance
NEAREST_CROSSING = find_nearest_crossing_manhattan(LINE_CROSSINGS)
if NEAREST_CROSSING[1] > 0:
    print("Nearest crossing found at {0}, distance {1}".format(
        NEAREST_CROSSING[0].to_string(), NEAREST_CROSSING[1]))


#Part 2 of Day 3


class Crossing:
    """Defines a crossing as a coordinate and distance to it"""

    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.distance = 0
        self.is_distance_calculated = False

def increment_distance_to_crossings(map_data, coordinate, *args):
    """Increments distance to all crossings provided in args.
    args contains a list of crossing objects.
    """
    for v in args:
        for crossing in v:
            if crossing.is_distance_calculated:
                continue
            crossing.distance += 1
            if crossing.coordinate.x == coordinate.x and crossing.coordinate.y == coordinate.y:
                crossing.is_distance_calculated = True

def calculate_crossing_distances(map_data, crossing_coordinates, line):
    crossings = []
    for c in crossing_coordinates:
        crossings.append(Crossing(c.copy()))
    coordinate = Coordinate(0,0)
    for instruction in line:
        coordinate = instruction.walk(map_data, coordinate, increment_distance_to_crossings, crossings)

    return crossings

def find_lowest_signal_delay(map_data, line_crossings, lines):
    """Walks through the lines and calculates distance to each crossing for each line.
    Returns the a tuple of the crossing with shortest signal delay as (int, int)
    where first value is the index and second is the distance.
    """
    total_signal_delays = []
    line_a_crossings = calculate_crossing_distances(map_data, line_crossings, lines[0])
    line_b_crossings = calculate_crossing_distances(map_data, line_crossings, lines[1])

    for index in range(len(line_a_crossings)):
        total_signal_delays.append(line_a_crossings[index].distance)
        print("Line A crossing at {0} with distance {1}".format(
            line_a_crossings[index].coordinate.to_string(), line_a_crossings[index].distance))
    for index in range(len(line_b_crossings)):
        total_signal_delays[index] += line_b_crossings[index].distance
        print("Line B crossing at {0} with distance {1}".format(
            line_b_crossings[index].coordinate.to_string(), line_b_crossings[index].distance))

    index_of_shortest_delay = -1
    shortest_delay = -1
    for index in range(len(total_signal_delays)):
        signal_delay = total_signal_delays[index]
        if LOG_LEVEL >= 1:
            print("Signal delay to crossing is {0}".format(signal_delay))
        if index_of_shortest_delay < 0 or signal_delay < shortest_delay:
            index_of_shortest_delay = index
            shortest_delay = signal_delay

    return (index_of_shortest_delay, shortest_delay)


#Find the crossing with lowest signal delay
NEAREST_CROSSING = find_lowest_signal_delay(LINE_MAP, LINE_CROSSINGS, LINES)
print("Crossing with lowest signal delay is at {0} with total combined signal delay {1}".format(
    LINE_CROSSINGS[NEAREST_CROSSING[0]].to_string(), NEAREST_CROSSING[1]))