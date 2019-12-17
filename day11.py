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

#Part 1 of Day 11


def run(program, input_parameters, map_data, start_position, start_direction, log_level):
    """Runs the intcode program with given data and starting parameters."""

    position = start_position
    direction = start_direction
    previous_position = position
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
            print(f"Total painted tiles now: {len(map_data)}, panel color at {position} is {current_color}")

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

        if log_level >= 1:
            print(f"Painted {output[0]} at {previous_position}, turned {output[1]}, " +
                  f"moved to direction {direction}, position now {position}.")

    print(f"Finished painting at position {position}, painted over {len(map_data)} tiles in total")

def get_int_list_input(prompt, invalid_prompt):
    """Get integer list input from user, returns a tuple (is_valid, input_list)"""

    input_list = []
    is_input_valid = False

    while not is_input_valid:
        is_input_valid = True
        input_text = input(prompt)

        #Empty input is valid too
        if len(input_text) == 0:
            break

        try:
            for txt in input_text.split(","):
                input_list.append(int(txt))
        except ValueError:
            input_list = []
            is_input_valid = False

            if invalid_prompt != None:
                print(invalid_prompt.format(input_text))
            else:
                break

    return (is_input_valid, input_list)


#Program


def play(input_file, input_parameters, log_level):
    """Program entry point"""


    #Initialize and read input

    
    input_strings = input_file.readline().split(",")

    program = []
    for i in input_strings:
        program.append(int(i))

    map_data = {}
    start_position = (0,0)


    #Run the program

    
    run(program.copy(), input_parameters, map_data, start_position, DIR_UP, log_level)
