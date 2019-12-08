"""Advent of Code 2019 - Day 7"""
import itertools
from modules import intcode_computer


#Global definitions


def run(program, input_parameters, stop_at_non_zero_output, log_level):
    """Runs program for each amplifier"""
    
    if log_level >= 1:
        print(f"Run for sequence {input_parameters}")

    output = 0

    for i in range(len(input_parameters)):
        if log_level >= 2:
            print(f"Run for amplifier {i}")

        retval = intcode_computer.run(program.copy(), [input_parameters[i], output], stop_at_non_zero_output, log_level)

        if retval[0] > 0:
            output = 0
            break

        output = retval[1]

    return output


#Part 1 of Day 7





#Part 2 of Day 7





#Program

    
def play(input_parameters, log_level):
    """Program entry point"""


    #Initialize and read input


    input_file = open("data/day7input.txt", "r")
    input_strings = input_file.readline().split(",")

    program = []
    for i in input_strings:
        program.append(int(i))


    #Run the program


    if len(input_parameters) < 5:
        #Discard given input and generate all possible input permutations,
        #where no value is repeated within a sequence, thanks itertools!
        input_parameters = itertools.permutations(range(5))
    else:
        input_parameters = [input_parameters]

    output = 0
    highest_output_value = -1
    highest_output_sequence = None
    for sequence in input_parameters:
        output = run(program, sequence, False, log_level)
        if output > highest_output_value:
            highest_output_sequence = sequence
            highest_output_value = output

    #txt = input("Choose part 1 or 2 (defaults to 1): ")
    #if txt == "1":
    #    output = run(program.copy(), input_parameters[0], True, log_level)
        
    print(f"Output is {highest_output_value} from sequence {highest_output_sequence}")
