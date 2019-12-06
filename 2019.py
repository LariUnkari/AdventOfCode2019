"""Advent of Code 2019 Solutions
Author: Lari Unkari
"""

import day1
import day2
import day3
import day4

def get_input():
    print("Select day (1-4), or type exit, then press enter")
    return input("input: ")

LOG_LEVEL = 1

USER_INPUT = get_input()
while USER_INPUT != "exit":
    if USER_INPUT == "1":
       day1.play(LOG_LEVEL)
    elif USER_INPUT == "2":
        day2.play(LOG_LEVEL)
    elif USER_INPUT == "3":
        day3.play(LOG_LEVEL)
    elif USER_INPUT == "4":
       day4.play(LOG_LEVEL)
    else:
        print(f"Unhandled day {USER_INPUT} given!")
        
    USER_INPUT = get_input()

print("Goodbye and Merry Christmas!")