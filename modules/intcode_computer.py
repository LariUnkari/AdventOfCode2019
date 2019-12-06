"""Intcode Computer Logic"""


def run(data, input, logLevel):
    """Runs intcode program with standard input and returns a tuple (stop_code, output)"""

    if logLevel >= 1:
        print(f"Run program with input {input}!")
        
    output = 0
    position = 0
    stop_code = 0
    while stop_code == 0:
        retval = process(data, position, input, logLevel)
        stop_code = retval[0]

        if stop_code == 0:
            output = retval[1]
            position = retval[2]

            if logLevel >= 2:
                print(f"Moved to position {position}, output is {output}")
        else:
            if logLevel >= 2:
                print(f"Terminating, stop code {stop_code}")

    return (stop_code, output)

def run_with_noun_verb(data, noun, verb, finalValuePosition, logLevel):
    """Runs intcode program with custom noun and verb values
    and outputs final value from given position
    """

    data[1] = noun
    data[2] = verb

    if logLevel >= 1:
        print(f"Run program with noun={noun}, verb={verb}! Final value position is {finalValuePosition}")

    retval = run(data, 0, logLevel)
    if retval[0] == 0:
        return data[finalValuePosition]
    else:
        return -1

def process(data, position, input, logLevel):
    """Process intcode program from given position, returns (stop_code, output, position)"""
    
    output = 0
    opcode = data[position]
    stop_code = 0

    if logLevel >= 3:
        print(f"opcode {opcode} found at position {position}")

    if opcode == 1:
        add(data, data[position + 1], data[position + 2], data[position + 3], logLevel)
        position += 4
    elif opcode == 2:
        mul(data, data[position + 1], data[position + 2], data[position + 3], logLevel)
        position += 4
    elif opcode == 3:
        store(data, data[position + 1], input, logLevel)
        position += 2
    elif opcode == 4:
        output = read(data, data[position + 1], logLevel)
        position += 2
    elif opcode == 99:
        stop_code = -1
    else:
        print(f"Unhandled opcode {opcode} at position {position}!")
        stop_code = 1
  
    return (stop_code, output, position) #Continue

def add(data, posA, posB, target, logLevel):
    """Adds values at posA and posB together and outputs the new value to target position"""

    value = data[posA] + data[posB]
    data[target] = value

    if logLevel >= 3:
        print(f"[{posA}] {data[posA]} + [{posB}] {data[posB]} = {value} [{target}]")

def mul(data, posA, posB, target, logLevel):
    """Multiplies values at posA and posB together and outputs the new value to target position"""

    value = data[posA] * data[posB]
    data[target] = value

    if logLevel >= 3:
        print(f"[{posA}] {data[posA]} * [{posB}] {data[posB]} = {value} [{target}]")

def store(data, target, value, logLevel):
    """Stores given input value to target position"""

    if logLevel >= 3:
        print(f"[{target}] = {value}")

    data[target] = value

def read(data, target, logLevel):
    """Reads from given target position and returns it"""

    if logLevel >= 3:
        print(f"Value at position {target} is {data[target]}")

    return data[target]
