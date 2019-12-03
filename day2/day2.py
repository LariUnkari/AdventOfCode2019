def process(map, position):
  opcode = map[position]

  txt = "opcode {0} found at position {1}"
  print(txt.format(opcode, position))

  if (opcode == 1):
    add(map, map[position + 1], map[position + 2], map[position + 3])
  elif (opcode == 2):
    mul(map, map[position + 1], map[position + 2], map[position + 3])
  else:
    if (opcode != 99):
      print("Unhandled opcode!")

    return 1 #Stop
  
  return 0 #Continue

def add(map, posA, posB, target):
  value = map[posA] + map[posB]
  map[target] = value

  txt = "[{0}] {1} + [{2}] {3} = {4} [{5}]"
  print(txt.format(posA, map[posA], posB, map[posB], value, target))

def mul(map, posA, posB, target):
  value = map[posA] * map[posB]
  map[target] = value

  txt = "[{0}] {1} * [{2}] {3} = {4} [{5}]"
  print(txt.format(posA, map[posA], posB, map[posB], value, target))


#Part 1 of Day 2


print("Day 2 begins!")
print("Gravity assist computer down!")

#Initialize and read input
file = open("input.txt", "r")
inputs = file.read().split(",")
txt = "Intcode input has {0} positions"
print(txt.format(len(inputs)))

intCodeMap = []
for i in inputs:
  intCodeMap.append(int(i))

#Restore 1202 program alarm
intCodeMap[1] = 12
intCodeMap[2] = 2

#Begin processing
position = 0
while process(intCodeMap, position) == 0:
  position += 4
  txt = "Moved to position {0}"
  print(txt.format(position))

#Finish processing
print("Processing complete!")
position = 0

txt = "Final value at position {0} is {1}"
print(txt.format(position, intCodeMap[position]))