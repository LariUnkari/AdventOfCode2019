#Input expected to be of type int
def calculateFuelRequiredForMass(mass):
    return int(mass / 3) - 2

#Input expected to be of type int
def calculateFuelRequiredForFuel(fuel):
    sumOfExtraFuel = 0
    extraFuel = 0

    while fuel > 0:
        extraFuel = calculateFuelRequiredForMass(fuel)

        #Check if extra fuel needs to be added to the sum
        if extraFuel <= 0:
            #txt = "Fuel mass of {0} requires a non-positive {1} mass of fuel, wishing really hard will suffice"
            #print(txt.format(fuel, extraFuel))
            break

        #Add the extra fuel requirement to the sum
        sumOfExtraFuel += extraFuel
        #txt = "Fuel mass of {0} requires extra {1} mass of fuel, sum is {2}"
        #print(txt.format(fuel, extraFuel, sumOfExtraFuel))
        fuel = extraFuel

    return sumOfExtraFuel


def play(input_parameters, log_level):
    

    #Initialize and read input


    print("Day 1 begins!")
    file = open("data/day1input.txt", "r")


    #Part 1 of Day 1


    print("Rocket requires fuel for each module.")
    moduleFuelRequirements = []
    totalFuel = 0

    fuel = 0
    mass = 0
    for i in file:
        mass = int(i)
        fuel = calculateFuelRequiredForMass(int(mass))
        if log_level >= 1:
            txt = "Fuel required by module {0} (mass {1}) is {2}"
            print(txt.format(len(moduleFuelRequirements), mass, fuel))
        moduleFuelRequirements.append(fuel)

    #Calculate total sum of fuel required
    for moduleFuel in moduleFuelRequirements:
        totalFuel += moduleFuel

    txt = "Total fuel needed by rocket is {0}"
    print(txt.format(totalFuel))


    #Part 2 of Day 1


    print("Oops! Fuel has mass and requires fuel too!")
    finalFuel = 0

    fuel = 0
    for index in range(len(moduleFuelRequirements)):
        moduleFuel = moduleFuelRequirements[index]
        fuel = calculateFuelRequiredForFuel(moduleFuel)
        if log_level >= 1:
            txt = "Extra fuel required by fuel of module {0} (mass {1}) is {2}"
            print(txt.format(index, moduleFuel, fuel))
        moduleFuelRequirements[index] = moduleFuel + fuel

    for moduleFuel in moduleFuelRequirements:
        finalFuel += moduleFuel

    txt = "Final fuel needed by rocket is {0} while module masses required only {1}"
    print(txt.format(finalFuel, moduleFuel))