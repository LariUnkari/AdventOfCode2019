"""Advent of Code 2019 - Day 9"""
from modules import intcode_computer


#Global definitions


#Part 1 of Day 7


def part_1_solution(program, input_parameters, log_level):
    """Returns a code"""

    retval = intcode_computer.run(program, 0, input_parameters, 0, 0, False, log_level)
    output = retval[1]
    print(f"Output is {output}")

#Program
    

def play(input_file, input_parameters, log_level):
    """Program entry point"""


    #Initialize and read input


    input_strings = input_file.readline().split(",")

    program = []
    for i in input_strings:
        program.append(int(i))


    #Run the program

    
    part_1_solution(program.copy(), input_parameters, log_level)
    