#Definitions
LogLevel = 1
CoordinateStringFormat = "{0},{1}"
LineMap = {}
LineCrossings = []

class LineInstruction:
  def __init__(self, lineIndex, direction, length):
    self.lineIndex = lineIndex
    self.direction = direction
    self.length = length
    if LogLevel >= 2:
      txt = "[{0}]LineInstruction(dir={1}, len={2})"
      print(txt.format(lineIndex, direction, length))

def SetLineAtCoordinate(x, y, doRegisterCrossing, logLevel):
  coordinate = CoordinateStringFormat.format(x, y)
  if doRegisterCrossing:
    if coordinate in LineMap:
      if LineMap[coordinate] == True:
        LineCrossings.append(coordinate)
        if logLevel >= 1:
          txt = "Lines cross at {0}"
          print(txt.format(coordinate))
  else:
    LineMap[CoordinateStringFormat.format(x, y)] = True

def DrawLineOnMap(lineInstructions, doRegisterCrossing, logLevel):
  x = 0
  y = 0
  SetLineAtCoordinate(x, y, doRegisterCrossing, logLevel)
  for instruction in lineInstructions:
    if instruction.direction == "U":
      for index in range(instruction.length):
        y += 1
        if logLevel >= 2:
          txt = "Moved up to {0},{1}"
          print(txt.format(x, y))
        SetLineAtCoordinate(x, y, doRegisterCrossing, logLevel)
    elif instruction.direction == "R":
      for index in range(instruction.length):
        x += 1
        if logLevel >= 2:
          txt = "Moved right to {0},{1}"
          print(txt.format(x, y))
        SetLineAtCoordinate(x, y, doRegisterCrossing, logLevel)
    if instruction.direction == "D":
      for index in range(instruction.length):
        y -= 1
        if logLevel >= 2:
          txt = "Moved down to {0},{1}"
          print(txt.format(x, y))
        SetLineAtCoordinate(x, y, doRegisterCrossing, logLevel)
    elif instruction.direction == "L":
      for index in range(instruction.length):
        x -= 1
        if logLevel >= 2:
          txt = "Moved left to {0},{1}"
          print(txt.format(x, y))
        SetLineAtCoordinate(x, y, doRegisterCrossing, logLevel)

#Initialize and read input


file = open("input.txt", "r")
inputs = [ file.readline().split(","), file.readline().split(",") ]

lineInstructions = []
for index in range(len(inputs)):
  lineInfo = []

  for lineInput in inputs[index]:
    lineInstruction = LineInstruction(index, lineInput[0], int(lineInput[1:]))
    lineInfo.append(lineInstruction)

  lineInstructions.append(lineInfo)


#Part 1 of Day 3


#Draw the line on map, then register crossing on second line
DrawLineOnMap(lineInstructions[0], False, LogLevel)
DrawLineOnMap(lineInstructions[1], True, LogLevel)

shortestDistance = -1
nearestCrossingCoordinate = ""

distance = 0
splits = ""
x = 0
y = 0
for coordinate in LineCrossings:
  splits = coordinate.split(",")
  x = int(splits[0])
  y = int(splits[1])

  distance = abs(x) + abs(y)
  if distance <= 0:
    continue

  if shortestDistance < 0 or distance < shortestDistance:
    shortestDistance = distance
    nearestCrossingCoordinate = coordinate
    if LogLevel >= 1:
      txt = "New nearest crossing found at {0}, distance {1}"
      print(txt.format(coordinate, distance))
   
if shortestDistance > 0:
  txt = "Final nearest crossing found at {0}, distance {1}"
  print(txt.format(nearestCrossingCoordinate, shortestDistance))