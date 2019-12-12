"""Advent of Code 2019 - Day 7"""
import itertools
from modules import intcode_computer


#Global definitions


COUNT_AMPLIFIERS = 5

class Amplifier:
    """Holds saved states of intcode computer programs"""

    def __init__(self, name, program):
        self.name = name
        self.program = program
        self.reset()

    def reset(self):
        """Resets all saved parameters to default values, resets program too"""

        self.memory = self.program.copy()
        self.output = 0
        self.stop_code = 0
        self.code_position = 0
        self.input_position = 0
        self.input_parameters = []

    def add_input(self, input_value, log_level):
        """Adds an input parameter to the list, but doesn't move the input position."""

        self.input_parameters.append(input_value)
        if log_level >= 1:
            print(f"Amplifier[{self.name}]: Input parameters: {self.input_parameters}," +
                  f" input position: {self.input_position}")

    def run_program(self, log_level):
        """Runs program from memory based on saved parameters, returns an output value"""
        
        if log_level >= 1:
            next_input = self.input_parameters[self.input_position]
            print(f"Run program for amplifier {self.name}, next input: {next_input}")
            
        retval = intcode_computer.run(self.memory, self.code_position,
                                     self.input_parameters, self.input_position, False, log_level)
        
        self.stop_code = retval[0]
        self.output = retval[1][0] #First output is the only relevant output
        self.code_position = retval[2]
        self.input_position = retval[3]

        if self.stop_code > 0: #Error
            self.output = 0

        return self.output


#Part 1 of Day 7


def part_1():
    """Thanks to itertools it's really easy  getting permutations of values of given range,
    with no repeating values, in a nice list of sequences.
    """
    return itertools.permutations(range(5))


#Part 2 of Day 7


def part_2():
    """Thanks to itertools it's really easy  getting permutations of values of given range,
    with no repeating values, in a nice list of sequences.
    """
    return itertools.permutations(range(5, 10))


#Program

    
def play(input_file, input_parameters, log_level):
    """Program entry point"""


    #Initialize and read input


    input_strings = input_file.readline().split(",")

    program = []
    for i in input_strings:
        program.append(int(i))

    amplifiers = []
    for i in range(COUNT_AMPLIFIERS):
        amplifiers.append(Amplifier(chr(ord('A') + i), program))


    #Run the program

    
    input_sequences = [] #List of sequences for phase input

    if len(input_parameters) < COUNT_AMPLIFIERS:
        #Discard given input and generate all possible input permutations,
        #where no value is repeated within a sequence!
        print(f"Input parameter list too short: {len(input_parameters)} < {COUNT_AMPLIFIERS}")
        txt = input("Choose part 1 or 2 (defaults to 2): ")
        if txt == "1":
            input_sequences = part_1()
        else:
            input_sequences = part_2()
    else:
        print(f"Input parameter list is valid: {len(input_parameters)} >= {COUNT_AMPLIFIERS}")
        input_sequences = [input_parameters] #Just make a list of a single sequence from parameters

    output_value = 0
    highest_output_value = -1
    highest_output_sequence = None

    #Run each sequence for all amps until they're halted
    for sequence in input_sequences:

        #Input next phase sequence
        for i in range(len(amplifiers)):
            amplifiers[i].add_input(sequence[i], log_level)

        is_halted = False
        while not is_halted:
            is_halted = True
            for amp in amplifiers:
                if amp.stop_code > -99 and amp.stop_code <= 0:
                    is_halted = False #Even one amp unhalted means we don't stop
                    amp.add_input(output_value, log_level)
                    output_value = amp.run_program(log_level)

        if output_value > highest_output_value:
            highest_output_sequence = sequence
            highest_output_value = output_value

        #Reset the output and amps for next sequence
        output_value = 0
        for amp in amplifiers:
            amp.reset()
        
    print(f"Highest output is {highest_output_value} from phase sequence {highest_output_sequence}")
    