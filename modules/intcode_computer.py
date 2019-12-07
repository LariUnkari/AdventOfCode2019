"""Intcode Computer Logic"""


#Operations


def op_add(data, a, b, target, log_level):
    """Adds values at posA and posB together and outputs the new value to target position"""

    value = a + b

    if log_level >= 3:
        print(f"Add operation, [{target}] = {value} ({a} + {b})")
        
    data[target] = value

def op_mul(data, a, b, target, log_level):
    """Multiplies values at posA and posB together and outputs the new value to target position"""

    value = a * b

    if log_level >= 3:
        print(f"Multiply operation, [{target}] = {value} ({a} * {b})")
        
    data[target] = value

def op_input(data, target, value, log_level):
    """Stores given input value to target position"""

    if log_level >= 3:
        print(f"Store operation, [{target}] = {value}")

    data[target] = value

def op_output(param, log_level):
    """Reads given input parameter and returns it, really exists just for debugging"""

    if log_level >= 3:
        print(f"Output operation: setting value {param} into output")

    return param

def op_jump_if_true(position, value, target, log_level):
    """If input value is non-zero, returns difference to target from position, otherwise returns 0"""

    result = target - position if value > 0 else 0

    if log_level >= 3:
        print(f"Jump-if-True operation, position={position}, input={value}, target={target}, result={result}")

    return result

def op_jump_if_false(position, value, target, log_level):
    """If input value is non-zero, returns difference to target from position, otherwise returns 0"""

    result = target - position if value == 0 else 0

    if log_level >= 3:
        print(f"Jump-if-False operation, position={position}, input={value}, target={target}, result={result}")

    return result

def op_less_than(data, a, b, target, log_level):
    """If a is less than b, stores 1 in target position, otherwise stores 0"""

    value = 1 if a < b else 0

    if log_level >= 3:
        print(f"Less-than operation, [{target}] = {value}, ({a} < {b})")
        
    data[target] = value

def op_equals(data, a, b, target, log_level):
    """If a is equal to b, stores 1 in target position, otherwise stores 0"""

    value = 1 if a == b else 0

    if log_level >= 3:
        print(f"Equals operation, [{target}] = {value}, ({a} == {b})")
        
    data[target] = value


#Support functions


def get_digit(number, n):
    """Gets the digit from given number, at index n from right to left"""
    return number // 10**n % 10

def get_opcode_with_params(value):
    """Extracts opcode and parameter modes from given instruction value, returns a tuple (int, int[])"""
    opcode = get_digit(value, 0) + 10 * get_digit(value, 1)
    modes = []
    for i in range(2, 5):
        modes.append(get_digit(value, i))

    return (opcode, modes)

def is_write_instruction(opcode):
    """Checks given opcode and returns True if it's a write instruction"""
    return (opcode >= 1 and opcode <= 3) or (opcode == 7 or opcode == 8)

def validate_opcode(opcode):
    """Checks given opcode and returns a stop code, where non-zero means it is invalid"""

    if opcode == 99:
        print(f"Stop opcode {opcode}!")
        return -1
    
    if opcode < 1 or opcode > 8:
        print(f"Invalid opcode {opcode}!")
        return 1

    return 0


#Process functions


def process_parameters(opcode, position, data, modes, log_level):
    """Processes data from position to extract params for given opcode, returns a list of ints.
    Assumes modes is an int list. If shorter than range, mode 0 is assumed for each missing value.
    """

    length = 3 #Defaults to 3, since it's most common
    if opcode == 3 or opcode == 4: #input and output
        length = 1
    elif opcode == 5 or opcode == 6: #jump if true/false
        length = 2

    params = data[position:position+length]

    #Write instructions force the last param to be a position, therefore read as is (fake immediate mode)
    if is_write_instruction(opcode):
        modes[length - 1] = 1

    if log_level >= 2:
        print(f"params[{position}:{position+length}]={params}, modes={modes}")
        
    for i in range(length):
        mode = modes[i] if i < len(modes) else 0 #Assume 0 for missing mode values
        if mode == 0:
            params[i] = data[params[i]] #Position mode, get from data at param value position
        #else:
            #Immediate mode, use param directly

    return params

def process_instruction(data, position, input, log_level):
    """Process intcode program from given position, returns (stop_code, output, position)"""
    
    output = 0

    instruction = get_opcode_with_params(data[position])
    opcode = instruction[0]
    stop_code = validate_opcode(opcode)

    if stop_code != 0:
        print(f"Halting at position {position}")
        return (stop_code, output, position) #Stop

    modes = instruction[1]

    if log_level >= 2:
        print(f"opcode {opcode} and modes {modes} found at position {position} (value={data[position]})")
       
    params = process_parameters(opcode, position + 1, data, modes, log_level)
    move = 0

    if log_level >= 3:
        print(f"params {params}")

    if opcode == 1:
        op_add(data, params[0], params[1], params[2], log_level)
    elif opcode == 2:
        op_mul(data, params[0], params[1], params[2], log_level)
    elif opcode == 3:
        op_input(data, params[0], input, log_level)
    elif opcode == 4:
        output = op_output(params[0], log_level)
    elif opcode == 5:
        move = op_jump_if_true(position, params[0], params[1], log_level) #Jump overrides move
    elif opcode == 6:
        move = op_jump_if_false(position, params[0], params[1], log_level) #Jump overrides move
    elif opcode == 7:
        op_less_than(data, params[0], params[1], params[2], log_level)
    elif opcode == 8:
        op_equals(data, params[0], params[1], params[2], log_level)
    else:
        print(f"Unhandled opcode {opcode} at position {position}!")
        stop_code = 1

    #By default, move position by 1 + param count
    if move == 0:
        move = 1 + len(params) 

    if log_level >= 2:
        print(f"Moving {move} positions")

    position += move
        
    return (stop_code, output, position) #Continue


#Run commands


def run(data, input, stop_at_non_zero_output, log_level):
    """Runs intcode program with standard input and returns a tuple (stop_code, output)"""

    if log_level >= 1:
        print(f"Run program with input {input} and data of length {len(data)}!")
        
    output = 0
    position = 0
    stop_code = 0
    while stop_code == 0:
        retval = process_instruction(data, position, input, log_level)
        stop_code = retval[0]

        if stop_code == 0:
            output = retval[1]
            position = retval[2]

            if stop_at_non_zero_output and output != 0:
                print("Non-zero output {output} detected, halt!")
                stop_code = 2
                break

            if log_level >= 1:
                print(f"Moved to position {position}, output is {output}")
        else:
            print(f"Terminating, stop code {stop_code}")

    return (stop_code, output)

def run_with_noun_verb(data, noun, verb, finalValuePosition, log_level):
    """Runs intcode program with custom noun and verb values
    and outputs final value from given position
    """

    data[1] = noun
    data[2] = verb

    if log_level >= 1:
        print(f"Run program with noun={noun}, verb={verb}! Final value position is {finalValuePosition}")

    retval = run(data, 0, False, log_level)
    if retval[0] == 0:
        return data[finalValuePosition]
    else:
        return -1
