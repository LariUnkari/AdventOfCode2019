"""Advent of Code 2019 - Day 4"""
import math

def get_digit(number, n):
    """Gets the digit from given number, at index n from left to right"""
    return number // 10**n % 10

def get_magnitude(number):
    """Calculates the order magnitude value of the given number"""
    return int(math.log10(number))

def get_next_valid_value(number):
    """Looks at the number and gets the next valud value"""
    
    value = number + 1

    #This is the last index of digits in the given number
    magnitude = get_magnitude(number)
    if LOG_LEVEL >= 2:
        print("Order of magnitude of value {0} is {1}".format(value, magnitude))

    found_digit_pair = False
    while not found_digit_pair:
        previous_digit_index = 0
        inverse_index = magnitude
        previous_digit_value = get_digit(value, inverse_index)

        for index in range(previous_digit_index + 1, magnitude + 1):
            inverse_index = magnitude - index
            digit = get_digit(value, inverse_index)

            if LOG_LEVEL >= 2:
                print("Evaluating value {0} at index {1}, digit={2}, previous={3}".format(
                    value, index, digit, previous_digit_value))

            if digit < previous_digit_value:
                increase = (previous_digit_value - digit) * 10**(inverse_index)
                value += increase

                if LOG_LEVEL >= 2:
                    print("Digit[{0}] value {1} is less than digit[{2}] value {3}, moved up by {4} to {5}".format(
                        index, digit, previous_digit_index, previous_digit_value, increase, value))

                found_digit_pair = True
            else:
                if digit == previous_digit_value:
                    if LOG_LEVEL >= 2:
                        print("Digit[{0}] value {1} is same as digit[{2}] value {3}!".format(
                            index, digit, previous_digit_index, previous_digit_value))

                    found_digit_pair = True

                previous_digit_value = digit

            previous_digit_index = index

        if not found_digit_pair:
            if LOG_LEVEL >= 1:
                print("Didn't find a pair, going for another pass!")
            value += 1

    return value

#Initialize and read input


LOG_LEVEL = 1

INPUT_FILE = open("input.txt", "r")
INPUT_STRINGS = INPUT_FILE.readline().split("-")

VALUE_MIN = int(INPUT_STRINGS[0])
VALUE_MAX = int(INPUT_STRINGS[1])


#Part 1 of Day 4


def seek_values(min, max):
    """Seeks values which adhere to rules and returns the count of valid values."""

    value_count = 0

    next = min
    previous = min
    while next < max:
        next = get_next_valid_value(previous)

        if next <= max:
            if LOG_LEVEL >= 1:
                print("Value[{0}] is {1}".format(value_count, next))
            value_count += 1

        previous = next

    return value_count

count_of_values = seek_values(VALUE_MIN, VALUE_MAX)
print("Found {0} correct values".format(count_of_values))