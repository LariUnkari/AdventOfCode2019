"""Advent of Code 2019 - Day 9"""
from modules import intcode_computer


#Global definitions


DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3

def apply_turn_to_direction(direction_from, turn,):
    """Applies a turn value to given direction integer.
    Positive means turning right, or clockwise, and negative the opposite.
    Returns the new direction as integer.
    """
    if turn == 0:
        return (direction_from - 1) % 4
    if turn == 1:
        return (direction_from + 1) % 4

    return direction_from

def apply_move_to_direction(x, y, direction):
    """Applies a single unit movement on grid from given position towards given direction.
    Returns new position tuple (x,y).
    """
    if direction == DIR_UP:
        return (x, y+1)
    if direction == DIR_RIGHT:
        return (x+1, y)
    if direction == DIR_DOWN:
        return (x, y-1)
    if direction == DIR_LEFT:
        return (x-1, y)

    print("Error, invalid direction {direction} provided!")
    return (x,y)

def run(program, input_parameters, map_data, start_position, start_direction, log_level):
    """Runs the intcode program with given data and starting parameters.
    Returns position information of the final painted area, all values are tuples (x,y):
    (final_position, corner_top_left, corner_bottom_right)
    """

    position = start_position
    direction = start_direction
    previous_position = position

    x_min, y_min = 0, 0
    x_max, y_max = 0, 0

    current_color = 0
    program_position = 0
    input_position = 0
    relative_base = 0

    stop_code = -3
    while stop_code < 0 and stop_code > -99:
        #Get color at position
        current_color = map_data[position] if position in map_data else 0
        input_parameters.append(current_color)

        if log_level >= 1:
            print(f"Panel color at {position} is {current_color}")

        retval = intcode_computer.run(program, program_position, input_parameters,
                                     input_position, relative_base, False, log_level - 1)

        #Process program data
        stop_code = retval[0]
        output = retval[1]
        program_position = retval[2]
        input_position = retval[3]
        relative_base = retval[4]

        #Process program output
        if log_level >= 2:
            print(f"Output is {output}")

        map_data[position] = output[0]
        previous_position = position
        direction = apply_turn_to_direction(direction, output[1])
        position = apply_move_to_direction(position[0], position[1], direction)

        if position[0] < x_min:
            x_min = position[0]
        if position[0] > x_max:
            x_max = position[0]
        if position[1] < y_min:
            y_min = position[1]
        if position[1] > y_max:
            y_max = position[1]

        if log_level >= 1:
            print(f"Painted {output[0]} at {previous_position}, turned {output[1]}, " +
                  f"moved to direction {direction}, position now {position}.")
            print(f"Total painted tiles now: {len(map_data)}, area dimensions: {x_max-x_min}x{y_max-y_min}")
            
    print(f"Finished painting at position {position}, painted over {len(map_data)} tiles in total")
    return (position, (x_min, y_min), (x_max, y_max))


#Part 1 of Day 11


def part_1(program, log_level):
    """Runs the program on empty data."""

    run(program, [], {}, (0,0), DIR_UP, log_level)


#Part 2 of Day 11


def part_2(program, log_level):
    """Runs the program on data with a single white tile at start position."""

    map_data = {}
    position = (0,0)
    map_data[position] = 1 #White at origo

    retval = run(program, [], map_data, position, DIR_UP, log_level)

    #Draw a picture with the data

    corner_top_left = retval[1]
    corner_bottom_right = retval[2]

    width = 1 + corner_bottom_right[0] - corner_top_left[0]
    height = 1 + corner_bottom_right[1] - corner_top_left[1]

    print(f"Printing image of dimensions {width}x{height}, offset {corner_top_left}")

    #Format image with zeros
    image_data = [i * 0 for i in range(1 + width * height)]

    #Draw all positions from map
    index = 0
    for pos in map_data:
        position = (pos[0] - corner_top_left[0], pos[1] - corner_top_left[1])
        index = position[1] * width + position[0]
        image_data[index] = map_data[pos]

    line = ""
    for y in reversed(range(height)):
        index = y * width
        for pixel in image_data[index:index+width]:
            line += '#' if pixel == 1 else ' '
        print(line)
        line = ""

#Program


def play(input_file, input_parameters, log_level):
    """Program entry point"""


    #Initialize and read input

    
    input_strings = input_file.readline().split(",")

    program = []
    for i in input_strings:
        program.append(int(i))


    #Run the program

    
    user_input = input("Choose part 1 or 2 solution (defaults to 2): ")
    if user_input == "1":
        part_1(program.copy(), log_level)
    else:
        part_2(program.copy(), log_level)
