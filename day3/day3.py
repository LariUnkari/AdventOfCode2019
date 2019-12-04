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

    def draw_on_map(self, map_data, coordinate, do_register_crossing):
        """Runs through line instructions and marks each passed coordinate down.
        Alternatively checks if a crossing was found and marks that up
        """
        if self.direction == "U":
            for i in range(self.length):
                coordinate.y += 1
                if LOG_LEVEL >= 2:
                    print("Moved up {0}/{1} to {2}".format(i, self.length, coordinate.to_string()))
                set_line_at_coordinate(map_data, coordinate, do_register_crossing)
        elif self.direction == "R":
            for i in range(self.length):
                coordinate.x += 1
                if LOG_LEVEL >= 2:
                    print("Moved right {0}/{1} to {2}".format(i, self.length, coordinate.to_string()))
                set_line_at_coordinate(map_data, coordinate, do_register_crossing)
        if self.direction == "D":
            for i in range(self.length):
                coordinate.y -= 1
                if LOG_LEVEL >= 2:
                    print("Moved down {0}/{1} to {2}".format(i, self.length, coordinate.to_string()))
                set_line_at_coordinate(map_data, coordinate, do_register_crossing)
        elif self.direction == "L":
            for i in range(self.length):
                coordinate.x -= 1
                if LOG_LEVEL >= 2:
                    print("Moved left {0}/{1} to {2}".format(i, self.length, coordinate.to_string()))
                set_line_at_coordinate(map_data, coordinate, do_register_crossing)

        return coordinate

def set_line_at_coordinate(map_data, coordinate, do_register_crossing):
    """Marks down that a line passes over a coordinate.
    Optionally adds a crossing instead if found to exist already
    """

    cs = coordinate.to_string()
    if do_register_crossing:
        if cs in map_data:
            if LOG_LEVEL >= 1:
                print("Coordinate {0} exists in map!".format(cs))
            if map_data[cs]:
                LINE_CROSSINGS.append(coordinate.copy())
                if LOG_LEVEL >= 1:
                    print("Lines cross at {0}".format(cs))
    else:
        map_data[coordinate.to_string()] = True


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


def draw_lines(map_data, line_a, line_b):
    """Draw lines on map and marks crossings"""

    #Draw the line on map, then register crossing on second line
    #No need to register starting point crossings
    coordinate = Coordinate(0,0)
    for instruction in line_a:
        coordinate = instruction.draw_on_map(map_data, coordinate, False)

    coordinate = Coordinate(0,0)
    for instruction in line_b:
        coordinate = instruction.draw_on_map(map_data, coordinate, True)

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


#Draw first
draw_lines(LINE_MAP, LINES[0], LINES[1])

#Find the nearest in manhattan distance
NEAREST_CROSSING = find_nearest_crossing_manhattan(LINE_CROSSINGS)
if NEAREST_CROSSING[1] > 0:
    print("Nearest crossing found at {0}, distance {1}".format(
        NEAREST_CROSSING[0].to_string(), NEAREST_CROSSING[1]))


#Part 2 of Day 3


#Trace along the lines to all crossings and tally the distance along the line
#Sum up the line distances to each crossing and find out which one has the
#Smallest distance sum, that is the answer