"""Advent of Code 2019 Solutions
Author: Lari Unkari
"""

import day1
import day2
import day3
import day4
import day5
import day6
import day7
import day8


#Definitions


DAY_COUNT = 8

def get_day_input():
    """Takes in user input for day choice"""

    print(f"Select day (1-{DAY_COUNT}), then press enter.\nEnter an empty input or 'exit' to end program")

    return input("Choose the day: ")

def get_int_list_input(prompt, invalid_prompt):
    """Get integer list input from user"""

    input_list = []
    is_input_valid = False

    while not is_input_valid:
        is_input_valid = True
        input_text = input(prompt)

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

    if is_input_valid: #Always return at least a list of a single zero on valid input (can be empty)
        return (True, input_list if len(input_list) > 0 else [0])

    return (False, [])


def get_int_input(prompt, invalid_prompt):
    """Get integer input from user"""

    input_value = 0
    is_input_valid = False
    while not is_input_valid:
        txt = input(prompt)

        if len(txt) == 0:
            break

        try:
            input_value = int(txt)
            is_input_valid = True
        except ValueError:
            if invalid_prompt != None:
                print(invalid_prompt.format(input_value))
            else:
                break

    return (is_input_valid, input_value)

def get_program_and_input(input_string):
    """Returns a day solution program and input as tuple (module, input_file). If invalid, returns (None, None)"""
    
    mod = None
    filepath = "data/day{0}input.txt"

    try:
        value = int(input_string)

        if value < 1:
            print(f"Invalid day value {value} given!")
        elif value > DAY_COUNT:
            print(f"Day {value} has not been reached yet!")
        else:
            if value == 1:
                mod = day1
            elif value == 2:
                mod = day2
            elif value == 3:
                mod = day3
            elif value == 4:
                mod = day4
            elif value == 5:
                mod = day5
            elif value == 6:
                mod = day6
            elif value == 7:
                mod = day7
            elif value == 8:
                mod = day8
    except ValueError:
        print(f"Invalid input {input_string} given!")
        return (None, None)

    return (mod, open(filepath.format(value), "r"))


#Program


USER_INPUT = "0"

while True:
    USER_INPUT = get_day_input()
    
    if len(USER_INPUT) == 0 or USER_INPUT.strip() == "exit":
        break

    params = get_program_and_input(USER_INPUT)
    if params != None:
        module = params[0]
        if module == None:
            print(f"No module found for {USER_INPUT}")
            break

        input_file = params[1]
        if input_file == None:
            print(f"No input file found for {USER_INPUT}")
            break

        #Input is a Tuple of (was_parse_success, list_of_int_values)
        program_input = get_int_list_input("Program input: ",
            "Invalid input {0}, try again or press enter without input to exit!")

        if not program_input[0]:
            break

        print(f"Input value list[0-{len(program_input[1])-1}]: {program_input[1]}")

        log_level_input = get_int_input("Log level (defaults to level zero): ", None)

        module.play(params[1], program_input[1], log_level_input[1] if log_level_input[0] else 0)

print("Goodbye and Merry Christmas!")