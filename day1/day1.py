def calculateFuelRequiredForMass(mass):
  return int(mass / 3) - 2

print("Day 1 begins!")

file = open("input.txt", "r")

fuel = 0
moduleFuelRequirements = []
for mass in file:
  fuel = calculateFuelRequiredForMass(float(mass))
  txt = "Fuel required by module {0} is {1}"
  print(txt.format(len(moduleFuelRequirements), fuel))
  moduleFuelRequirements.append(fuel)

totalFuel = 0
for moduleFuel in moduleFuelRequirements:
  totalFuel += moduleFuel

txt = "Total fuel needed by each module is {0}"
print(txt.format(totalFuel))