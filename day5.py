"""Advent of Code 2019 - Day 5"""
from modules import intcode_computer #Wow, we're using module packages now!


def play(log_level):


    #Initialize and read input


    input_file = open("data/day5input.txt", "r")
    input_strings = input_file.readline().split(",") #Only read first line

    program = []
    for i in input_strings:
        program.append(int(i))


    #Part 1 of Day 5


    #Input of 1 for air conditioner TEST run
    retval = intcode_computer.run(program.copy(), 1, True, log_level)
    output = retval[1]

    print(f"Output is {output}")


    #Part 2 of Day 5


    #Input of 8 for radiators TEST run
    retval = intcode_computer.run(program.copy(), 1, False, log_level)
    output = retval[1]

    print(f"Output is {output}")
