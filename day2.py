def run(data, noun, verb, finalValuePosition, log_level):
    data[1] = noun
    data[2] = verb

    if log_level >= 1:
        txt = "Run program with noun={0}, verb={1}! Final value position is {2}"
        print(txt.format(noun, verb, finalValuePosition))

    position = 0
    while process(data, position, log_level) == 0:
        position += 4
    
        if log_level >= 2:
            txt = "Moved to position {0}"
            print(txt.format(position))

    return data[finalValuePosition]

def process(data, position, log_level):
    opcode = data[position]

    if log_level >= 3:
        txt = "opcode {0} found at position {1}"
        print(txt.format(opcode, position))

    if opcode == 1:
        add(data, data[position + 1], data[position + 2], data[position + 3], log_level)
    elif opcode == 2:
        mul(data, data[position + 1], data[position + 2], data[position + 3], log_level)
    else:
        if opcode != 99:
            print("Unhandled opcode!")

        return 1 #Stop
  
    return 0 #Continue

def add(data, posA, posB, target, log_level):
    value = data[posA] + data[posB]
    data[target] = value

    if log_level >= 3:
        txt = "[{0}] {1} + [{2}] {3} = {4} [{5}]"
        print(txt.format(posA, data[posA], posB, data[posB], value, target))

def mul(data, posA, posB, target, log_level):
    value = data[posA] * data[posB]
    data[target] = value

    if log_level >= 3:
        txt = "[{0}] {1} * [{2}] {3} = {4} [{5}]"
        print(txt.format(posA, data[posA], posB, data[posB], value, target))


def play(input_file, input_parameters, log_level):


    #Initialize and read input


    inputs = input_file.read().split(",")

    program = []
    for i in inputs:
        program.append(int(i))


    #Part 1 of Day 2


    print("Day 2 begins!")
    print("Gravity assist computer down!")

    #Run program by restoring 1202 program alarm
    targetPosition = 0
    output = run(program.copy(), 12, 2, targetPosition, 1)

    txt = "Final value at position {0} is {1}"
    print(txt.format(targetPosition, output))


    #Part 2 of Day 2


    print("Finding correct noun and verb for moon gravity assist...")

    targetOutput = 19690720
    targetPosition = 0
    noun = 0
    verb = 0

    output = 0
    while verb < 100:
        output = run(program.copy(), noun, verb, targetPosition, 0)
        if output == targetOutput:
            break

    if noun < 99:
        noun += 1
    else:
        noun = 0
        verb += 1
  
    if output == targetOutput:
        txt = "Correct noun is {0} and verb {1}"
        print(txt.format(noun, verb))
    else:
        print("Correct values were not found...")

    finalValue = 100 * noun + verb
    txt = "Final value from correct noun and verb is {0}"
    print(txt.format(finalValue))