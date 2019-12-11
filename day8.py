"""Advent of Code 2019 - Day 8"""


#Global definitions


def parse_image_string(string_data, width, height, log_level):
    """Returns a nested list of ints, layer[row[column[]]], or None if failed to parse"""

    #Validate data
    input_parameters = width * height
    remainder = len(string_data) % input_parameters
    if remainder != 0:
        print(f"Layer size {input_parameters} ({width}*{height}) and data length {len(string_data)}" +
              f"mismatch by an offset of {remainder}!")
        return None

    #Calculate how many layers to expect
    layer_count = len(string_data) // input_parameters

    image_data = []
    layer_data = []
    row_data = []
    
    p = 0 #Pixel index
    for i in range(layer_count):
        if log_level >= 3:
            print(f"Parsing layer {i}/{layer_count}")
        for y in range(height):
            for x in range(width):
                row_data.append(int(string_data[p]))
                p += 1

            layer_data.append(row_data)
            row_data = []
            
        image_data.append(layer_data)
        layer_data = []

    return image_data

#Part 1 of Day 8


def get_default_image_params():
    """Returns the default day 8 part 1 image parameters width and height (int, int)."""

    return (25, 6)

def part_1_solution(image_data, layer_size, log_level):
    """Interprets the image data to find the solution for part 1. Outputs an int"""

    layer_with_fewest_zeros = -1
    lowest_zero_count = layer_size

    zero_count = 0
    for layer in range(len(image_data)):
        for row in image_data[layer]:
            for pixel in row:
                if pixel == 0:
                    zero_count += 1

        if log_level >= 2:
            print(f"Layer {layer} has {zero_count} zeros in it")
        if zero_count < lowest_zero_count:
            layer_with_fewest_zeros = layer
            lowest_zero_count = zero_count

        zero_count = 0

    if log_level >= 1:
        print(f"Layer {layer_with_fewest_zeros} has the lowest zero count {lowest_zero_count}")

    count_of_1s, count_of_2s = 0, 0
    for row in image_data[layer_with_fewest_zeros]:
        for pixel in row:
            if pixel == 1:
                count_of_1s += 1
            elif pixel == 2:
                count_of_2s += 1
                
    if log_level >= 1:
        print(f"Layer {layer_with_fewest_zeros} has {count_of_1s} 1s and {count_of_2s} 2s")

    return count_of_1s * count_of_2s


#Part 2 of Day 8


def part_2_solution(image_data, width, height, log_level):
    """Processes the image data to get the final image data, flattened to one layer."""
    
    final_image_data = []
    row = []
    
    pixel = -1
    for y in range(height):
        for x in range(width):
            #Go through the same pixel coordinate in all layers, from top to bottom

            for i in range(len(image_data)):
                pixel = image_data[i][y][x]
                if i == 0:
                    #First layer must always be appended
                    row.append(pixel)
                elif pixel < 2 and row[x] == 2:
                    #Overwrite if layer above is transparent
                    row[x] = pixel

                    if log_level >= 3:
                        print(f"Overwriting pixel {x},{y} with {pixel}")

        #Finished processing layers, set to data and reset for another row
        final_image_data.append(row)
        row = []

    return final_image_data


#Program

    
def play(input_file, input_parameters, log_level):
    """Program entry point"""


    #Initialize and read input


    if len(input_parameters) != 2:
        input_parameters = get_default_image_params()

    width = input_parameters[0]
    height = input_parameters[1]
        
    input_string = input_file.readline().strip()
    image_data = parse_image_string(input_string, width, height, log_level)

    if image_data == None:
        print("No image data parsed!")
        return

    if log_level >= 3:
        print("Image data:")

        for layer in range(len(image_data)):
            print(f"Image layer {layer}:")

            for row in image_data[layer]:
                txt = ""

                for pixel in row:
                    txt += str(pixel)

                print(txt)

    user_input = input("Choose part 1 or 2 solution (defaults to 2): ")
    if user_input == "1":
        output_value = part_1_solution(image_data, width * height, log_level)
        print(f"Answer to {user_input} is {output_value}")
    else:
        final_image_data = part_2_solution(image_data, width, height, log_level)

        print(f"Printing out final image:")
        txt = ""
        for row in range(height):
            for pixel in final_image_data[row]:
                txt += str(pixel) if pixel > 0 else " "
            
            print(f"{txt}")
            txt = ""