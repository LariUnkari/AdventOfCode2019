"""Advent of Code 2019 - Day 5"""
from modules import intcode_computer #Wow, we're using module packages now!


def play(log_level):


    #Initialize and read input


    input_file = "3,0,4,0,99" #open("data/day5input.txt", "r")
    input_strings = input_file.split(",") #input_file.readline().split(",") #Only read first line

    program = []
    for i in input_strings:
        program.append(int(i))


    #Part 1 of Day 5


    retval = intcode_computer.run(program.copy(), 5, log_level)
    output = retval[1]

    print(f"Output is {output}")
