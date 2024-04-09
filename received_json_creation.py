import json
import random
import string

def generate_random_color_name():
    shape_colors = ['white', 'black', 'red', 'blue', 'green', 'purple', 'brown', 'orange']
    return random.choice(shape_colors)

def generate_random_shape():
    shapes = ['circle', 'semicircle', 'quarter circle', 'triangle','rectangle', 'pentagon', 'star', 'cross']
    return random.choice(shapes)

def generate_random_letter_color():
    color_names = ['white', 'black', 'red', 'blue', 'green', 'purple', 'brown', 'orange']
    letter_color = random.choice(color_names)
    # Ensure letter color is different from color
    while True:
        new_letter_color = random.choice(color_names)
        if new_letter_color != letter_color:
            return new_letter_color

def generate_random_json(num_entries=5):
    data = {}
    category_name = 'to find'  # Change category name to 'to find'
    color = generate_random_color_name()
    letter_color = generate_random_letter_color()
    while color == letter_color:
        letter_color = generate_random_letter_color()
    value = {
        'color': color,
        'shape': generate_random_shape(),
        'letter_color': letter_color,
        'letter': random.choice(string.ascii_uppercase)
    }
    data[category_name] = value
    return data

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    num_entries = 1  # Change number of categories to 1
    file_path = '/home/sahil/Documents/test.py/received.json'

    # Generate random JSON data
    json_data = generate_random_json(num_entries)

    # Save JSON data to a file
    save_json(json_data, file_path)

    print(f"Random JSON data has been generated and saved to '{file_path}'.")

if __name__ == "__main__":
    main()
