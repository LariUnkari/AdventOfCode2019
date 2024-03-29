"""Advent of Code 2019 - Day 4"""
import math

def get_digit(number, n):
    """Gets the digit from given number, at index n from right to left"""
    return number // 10**n % 10

def get_magnitude(number):
    """Calculates the order magnitude value of the given number"""
    return int(math.log10(number))

def validate_digit_group(digit_value, digit_group_length, group_length_min, group_length_max, log_level):
    """Returns True if group length is within limits"""

    if group_length_max >= 0 and digit_group_length > group_length_max:
        if log_level >= 3:
            print("Digit {0} group count {1} exceeded maximum {2}, group disregarded!".format(
                digit_value, digit_group_length, group_length_max))
    elif digit_group_length >= group_length_min:
        if log_level >= 3:
            if group_length_max >= 0:
                print("Digit {0} group count {1} within limits {2}-{3}, valid group found!".format(
                    digit_value, digit_group_length, group_length_min, group_length_max))
            else:
                print("Digit {0} group count {1} exceeded minimum {2}, group disregarded!".format(
                    digit_value, digit_group_length, group_length_min))

        return True
    
    return False

def get_next_valid_value(number, group_length_min, group_length_max, log_level):
    """Looks at the number and gets the next valud value"""
    
    value = number + 1

    #This is the last index of digits in the given number
    magnitude = get_magnitude(number)
    if log_level >= 3:
        print("Order of magnitude of value {0} is {1}".format(value, magnitude))

    found_digit_group = False
    while not found_digit_group:
        digit_group_length = 1
        previous_digit_index = 0
        inverse_index = magnitude
        previous_digit_value = get_digit(value, inverse_index)

        for index in range(previous_digit_index + 1, magnitude + 1):
            inverse_index = magnitude - index
            digit = get_digit(value, inverse_index)

            if log_level >= 3:
                print("Evaluating value {0} at index {1}, digit={2}, previous={3}".format(
                    value, index, digit, previous_digit_value))

            #Check digit is not decreasing, and set current digit to previous if it did decrease
            if digit < previous_digit_value:
                increase = (previous_digit_value - digit) * 10**(inverse_index)
                value += increase

                if log_level >= 3:
                    txt = "Digit[{0}] value {1} is less than digit[{2}] value {3}, moved up by {4} to {5}"
                    print(txt.format(index, digit, previous_digit_index, previous_digit_value,
                                    increase, value))
                    
                digit = previous_digit_value

            #If no group has been found yet, check for it
            if not found_digit_group:
                #If match found, increment group length
                #Otherwise validate previous group and reset digit group counter
                if digit == previous_digit_value:
                    digit_group_length += 1

                    if log_level >= 3:
                        txt = "Digit[{0}] value {1} is same as digit[{2}] value {3}, group counter at {4}!"
                        print(txt.format(index, digit, previous_digit_index,
                                         previous_digit_value, digit_group_length))
                else:
                    if validate_digit_group(previous_digit_value, digit_group_length, group_length_min, group_length_max, log_level):
                        found_digit_group = True
                    else:
                        if log_level >= 3:
                            txt = "Digit[{0}] value {1} is not the same as digit[{2}] value {3}, resetting group counter!"
                            print(txt.format(index, digit, previous_digit_index, previous_digit_value))

                        digit_group_length = 1

            previous_digit_index = index
            previous_digit_value = digit

        #End of digit sequence, check digit group and move on if necessary
        if not found_digit_group:
            if validate_digit_group(previous_digit_value, digit_group_length, group_length_min, group_length_max, log_level):
                break

            if log_level >= 2:
                txt = "Didn't find a valid digit group in value {0}, going for next number!"
                print(txt.format(value))
            value += 1

    return value

def seek_values(value_min, value_max, group_length_min, group_length_max, log_level):
    """Seeks values which adhere to rules and returns the count of valid values."""

    #Validate range
    if group_length_min > group_length_max and group_length_max >= 0:
        print("Invalid group length range given: {0}-{1}".format(
            group_length_min, group_length_max))
        return 0

    if group_length_max >= 0:
        print("Seeking values from {0} to {1}, allowed group size is in range {2}-{3}".format(
            value_min, value_max, group_length_min, group_length_max))
    else:
        print("Seeking values from {0} to {1}, minimum allowed group size is {2}".format(
            value_min, value_max, group_length_min))

    value_count = 0

    next_value = value_min
    previous_value = value_min
    while next_value < value_max:
        next_value = get_next_valid_value(previous_value, group_length_min, group_length_max, log_level)

        if next_value <= value_max:
            if log_level >= 1:
                print("Value[{0}] is {1}".format(value_count, next_value))
            value_count += 1

        previous_value = next_value

    return value_count


def play(input_file, input_parameters, log_level):


    #Initialize and read input


    INPUT_STRINGS = input_file.readline().split("-")

    VALUE_MIN = int(INPUT_STRINGS[0])
    VALUE_MAX = int(INPUT_STRINGS[1])


    #Part 1 of Day 4


    COUNT_VALUES = seek_values(VALUE_MIN, VALUE_MAX, 2, -1, log_level)
    print("Found {0} possible values".format(COUNT_VALUES))


    #Part 2 of Day 4


    COUNT_VALUES = seek_values(VALUE_MIN, VALUE_MAX, 2, 2, log_level)
    print("Found {0} possible values".format(COUNT_VALUES))
