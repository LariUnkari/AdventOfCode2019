"""Intcode Computer Logic"""


#Operations


def op_add(data, a, b, target, log_level):
    """Adds values at posA and posB together and outputs the new value to target position"""

    value = a + b

    if log_level >= 3:
        print(f"Add operation, [{target}] = {value} ({a} + {b})")
        
    if validate_data_up_to_position(data, target, log_level):
        data[target] = value
    else:
        print(f"Unable to set value {value} at position {target}!")

def op_mul(data, a, b, target, log_level):
    """Multiplies values at posA and posB together and outputs the new value to target position"""

    value = a * b

    if log_level >= 3:
        print(f"Multiply operation: [{target}] = {value} ({a} * {b})")
        
    if validate_data_up_to_position(data, target, log_level):
        data[target] = value
    else:
        print(f"Unable to set value {value} at position {target}!")

def op_input(data, target, value, log_level):
    """Writes given input value to target position"""

    if log_level >= 3:
        print(f"Input operation: [{target}] = {value}")
        
    if validate_data_up_to_position(data, target, log_level):
        data[target] = value
    else:
        print(f"Unable to set value {value} at position {target}!")

def op_output(param, output_list, log_level):
    """Reads given input parameter and returns it, really exists just for debugging"""

    output_list.append(param)

    if log_level >= 3:
        print(f"Output operation: added value {param} into output: {output_list}")

def op_jump_if_true(position, value, target, log_level):
    """If input value is non-zero, returns difference to target from position, otherwise returns 0"""

    result = target - position if value > 0 else 0

    if log_level >= 3:
        print(f"Jump-if-True operation: position={position}, input={value}, target={target}, result={result}")

    return result

def op_jump_if_false(position, value, target, log_level):
    """If input value is non-zero, returns difference to target from position, otherwise returns 0"""

    result = target - position if value == 0 else 0

    if log_level >= 3:
        print(f"Jump-if-False operation: position={position}, input={value}, target={target}, result={result}")

    return result

def op_less_than(data, a, b, target, log_level):
    """If a is less than b, stores 1 in target position, otherwise stores 0"""

    value = 1 if a < b else 0

    if log_level >= 3:
        print(f"Less-than operation: [{target}] = {value}, ({a} < {b})")
        
    if validate_data_up_to_position(data, target, log_level):
        data[target] = value
    else:
        print(f"Unable to set value {value} at position {target}!")

def op_equals(data, a, b, target, log_level):
    """If a is equal to b, stores 1 in target position, otherwise stores 0"""

    value = 1 if a == b else 0

    if log_level >= 3:
        print(f"Equals operation: [{target}] = {value}, ({a} == {b})")
        
    if validate_data_up_to_position(data, target, log_level):
        data[target] = value
    else:
        print(f"Unable to set value {value} at position {target}!")

def op_adjust_relative_base(relative_base, change, log_level):
    """Adjusts the relative base by a value and returns it, really exists just for debugging"""

    new_base = relative_base + change
    if log_level >= 3:
        print(f"Adjust relative base operation: base changed by {change} from {relative_base} to {new_base}")

    return new_base


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

def get_data_value_at(data, position, log_level):
    """Gets data value at given position, creates new data entries if position was out of bounds.
    Returns a tuple (is_valid, value).
    """
    if position < 0 or not validate_data_up_to_position(data, position, log_level):
        return (False, 0)

    return (True, data[position])

def get_data_range_at(data, position_from, position_to, log_level):
    """Gets data range at given range, creates new data entries if either position was out of bounds.
    Returns a tuple (is_valid, value_list).
    """
    if position_from < 0 or position_to < 0 or position_from > position_to:
        return (False, 0)
    
    if not validate_data_up_to_position(data, position_to, log_level):
        return (False, 0)

    return (True, data[position_from:position_to])

def validate_data_up_to_position(data, position, log_level):
    """Makes sure data is readable up to given position.
    This is just a dirty list extension to set all values at zero.
    Returns True always, for now
    """
    
    if position >= len(data):
        if log_level >= 3:
            print(f"Data length {len(data)} is inadequate to reach position {position}")

        data.extend([x * 0 for x in range(len(data), position + 1)])

        if log_level >= 3:
            print(f"Data length extended to {len(data)}")

    return True

def is_write_instruction(opcode):
    """Checks given opcode and returns True if it's a write instruction"""
    return (opcode >= 1 and opcode <= 3) or (opcode == 7 or opcode == 8)

def validate_opcode(opcode, log_level):
    """Checks given opcode and returns a stop code, where non-zero means it is invalid"""

    if opcode == 99:
        if log_level >= 1:
            print(f"Stop opcode {opcode}!")

        return -99
    
    if opcode < 1 or opcode > 9:
        print(f"Invalid opcode {opcode}!")
        return 1

    return 0


#Process functions


def process_parameters(opcode, position, relative_base, data, modes, log_level):
    """Processes data from position to extract params for given opcode, returns a list of ints.
    Assumes modes is an int list. If shorter than range, mode 0 is assumed for each missing value.
    """

    length = 3 #Defaults to 3, since it's most common
    if opcode == 3 or opcode == 4 or opcode == 9: #input, output and set relative base
        length = 1
    elif opcode == 5 or opcode == 6: #jump if true/false
        length = 2

    retval = get_data_range_at(data, position, position + length, log_level)
    if not retval[0]:
        return []

    params = retval[1]

    #Write instructions force the last param to be a position, therefore read as is (fake immediate mode)
    if is_write_instruction(opcode):
        modes[length - 1] = 1

    if log_level >= 2:
        print(f"Before: params[{position}:{position+length}]={params}, modes={modes}")
        
    for i in range(length):
        mode = modes[i] if i < len(modes) else 0 #Assume 0 for missing mode values
        if mode == 0:
            #Position mode, get from data at param value position
            retval = get_data_value_at(data, params[i], log_level)

            if not retval[0]:
                return []

            params[i] = retval[1]
        elif mode == 2:
            #Relative mode, get from data at param value position offset by relative base
            print(f"Relative base offset by {relative_base}")
            retval = get_data_value_at(data, params[i] + relative_base, log_level)

            if not retval[0]:
                return []

            params[i] = retval[1]
        #else:
            #Immediate mode, use param directly
            
    if log_level >= 2:
        print(f"After: params[{position}:{position+length}]={params}, modes={modes}")

    return params

def process_instruction(data, position, input_parameters, input_position, relative_base, old_output, log_level):
    """Process intcode program from given position, returns (stop_code, output, position, input_position, relative_base)"""
    
    new_output = old_output.copy()

    instruction = get_opcode_with_params(data[position])
    opcode = instruction[0]
    stop_code = validate_opcode(opcode, log_level)

    #Stop if needed
    if stop_code != 0:
        if stop_code == -99: #Standard halt
            if log_level >= 1:
                print(f"Halting for program end code {stop_code} at position {position}")
        elif stop_code > 0:
            if log_level >= 1:
                print(f"Halting for error {stop_code} at position {position}")
        else:
            if log_level >= 1:
                print(f"Pausing for {stop_code} at position {position}")

        return (stop_code, new_output, position, input_position, relative_base)

    modes = instruction[1]

    if log_level >= 2:
        print(f"opcode {opcode} and modes {modes} found at position {position} (value={data[position]})")
       
    params = process_parameters(opcode, position + 1, relative_base, data, modes, log_level)
    move = 0

    if log_level >= 3:
        print(f"params {params}")

    if opcode == 1:
        op_add(data, params[0], params[1], params[2], log_level)
    elif opcode == 2:
        op_mul(data, params[0], params[1], params[2], log_level)
    elif opcode == 3:
        if input_position >= len(input_parameters):
            if log_level >= 1:
                print(f"No input queued, pausing for input!")
            stop_code = -3 #Stop to wait for input
            return (stop_code, new_output, position, input_position, relative_base)
        op_input(data, params[0], input_parameters[input_position], log_level)
        input_position += 1
    elif opcode == 4:
        op_output(params[0], new_output, log_level)
    elif opcode == 5:
        move = op_jump_if_true(position, params[0], params[1], log_level) #Jump overrides move
    elif opcode == 6:
        move = op_jump_if_false(position, params[0], params[1], log_level) #Jump overrides move
    elif opcode == 7:
        op_less_than(data, params[0], params[1], params[2], log_level)
    elif opcode == 8:
        op_equals(data, params[0], params[1], params[2], log_level)
    elif opcode == 9:
        relative_base = op_adjust_relative_base(relative_base, params[0], log_level)
    else:
        print(f"Unhandled opcode {opcode} at position {position}!")
        stop_code = 99

    #By default, move position by 1 + param count
    if move == 0:
        move = 1 + len(params) 

    if log_level >= 2:
        print(f"Moving {move} positions")

    position += move
        
    return (stop_code, new_output, position, input_position, relative_base) #Continue


#Run commands


def run(data, position, input_parameters, input_position, relative_base, stop_at_non_zero_output, log_level):
    """Runs intcode program with standard input.
    Returns a tuple (stop_code, output, position, input_position, relative_base).
    Output is a list of int values.
    """
    if log_level >= 1:
        print(f"Run program from position {position} with input {input_parameters} from " +
              f"input position {input_position} and data of length {len(data)}!")
        
    output = []
    stop_code = 0
    while stop_code == 0:
        retval = process_instruction(data, position, input_parameters, input_position, relative_base, output, log_level)

        stop_code = retval[0]
        output = retval[1]
        position = retval[2]
        input_position = retval[3]
        relative_base = retval[4]

        if stop_code == 0:
            if stop_at_non_zero_output:
                if len(output) > 0 and output[len(output) - 1] != 0:
                    print(f"Non-zero output {output} detected, halt!")
                    stop_code = 2
                    break

            if log_level >= 1:
                print(f"Moved to position {position}, input position is {input_position}")
        else:
            if stop_code == -99 or stop_code >= 1:
                if log_level >= 1:
                    print(f"Terminating, stop code {stop_code}")
            else:
                if log_level >= 1:
                    print(f"Pausing, stop code {stop_code}")

    return (stop_code, output, position, input_position, relative_base)

def run_with_noun_verb(data, noun, verb, finalValuePosition, log_level):
    """Runs intcode program with custom noun and verb values
    and outputs final value from given position
    """

    data[1] = noun
    data[2] = verb

    if log_level >= 1:
        print(f"Run program with noun={noun}, verb={verb}! Final value position is {finalValuePosition}")

    retval = run(data, 0, [], 0, 0, False, log_level)
    if retval[0] == 0:
        return data[finalValuePosition]
    else:
        return -1
