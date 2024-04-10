import json

shape_colors = ['white', 'black', 'red', 'blue', 'green', 'purple', 'brown', 'orange']

letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0']

shapes = ['circle', 'semicircle', 'quarter circle', 'triangle','rectangle', 'pentagon', 'star', 'cross']

color_names = ['white', 'black', 'red', 'blue', 'green', 'purple', 'brown', 'orange']

def generate_random_json(num_entries):
    data = {}
    category_name = 'to find'  

    value = {
        'color': color_names,
        'shape': shapes,
        'letter_color': color_names,
        'letter':letters
    }
    data[category_name] = value
    return data

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    num_entries = 1  
    file_path = '/home/sahil/Documents/test.py/received.json'
    json_data = generate_random_json(num_entries)
    save_json(json_data, file_path)
    print(f"Random JSON data has been generated and saved to '{file_path}'.")

if __name__ == "__main__":
    main()
