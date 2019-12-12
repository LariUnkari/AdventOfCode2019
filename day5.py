"""Advent of Code 2019 - Day 5"""
from modules import intcode_computer #Wow, we're using module packages now!


def run(program, input_parameter, stop_at_non_zero_output, log_level):
    retval = intcode_computer.run(program, 0, input_parameter, 0, stop_at_non_zero_output, log_level)
    output_list = retval[1]
    return output_list[len(output_list) - 1] #Last output is the only relevant output


def play(input_file, input_parameters, log_level):


    #Initialize and read input


    input_strings = input_file.readline().split(",") #Only read first line

    program = []
    for i in input_strings:
        program.append(int(i))


    #Run the program


    output = 0
    txt = input("Choose part 1 or 2 (defaults to 2): ")
    if txt == "1":
        output = run(program.copy(), input_parameters, True, log_level) #Input of 1 for air conditioner TEST run
    else:
        output = run(program.copy(), input_parameters, False, log_level)
        
    print(f"Output is {output}")
