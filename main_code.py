import json
import time
# import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class JSONFileChangeHandler(PatternMatchingEventHandler):
    def __init__(self, json1_path, json2_path, comparison_function,priority_order):
        self.json1_path = json1_path
        self.json2_path = json2_path
        self.comparison_function = comparison_function
        self.priority_order=priority_order
        super().__init__(patterns=[json2_path])

    def on_modified(self, event):
        print("Detected change in random.json. Running comparison...")
        json1 = load_json(self.json1_path)
        json2 = load_json(self.json2_path)
        self.comparison_function(json1, json2,self.priority_order)

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_similarity(json1, json2):
    attribute2 = list(json2.keys())[0]  # Assuming file 2 has only one attribute
    features1 = json1.values()
    features2 = json2[attribute2].values()
    matching_features = sum(1 for feature in features1 if feature in features2)
    totalfeature=len(features1)
    similarity = (matching_features / totalfeature) * 100 if totalfeature > 0 else 0
    return similarity

def compare_features(json1, json2, priority_order):
    similarities = {}
    highest_similarity = 0
    best_attribute = None
    best_attributes = []
    matching_features={}
    
    for attribute_name, features in json1.items():
        attribute_similarity = 0
        matching_features[attribute_name] = []  # Initialize list to store matching features for this attribute
        for key, value in features.items():
            if key in json2["to find"] and value == json2["to find"][key]:
                attribute_similarity += 1
                matching_features[attribute_name].append({key: value})
        attribute_similarity /= len(features)  # Normalize similarity to [0, 1]

        if attribute_similarity > highest_similarity:
            highest_similarity = attribute_similarity
            best_attribute = attribute_name
            equal_similarity_encountered = False  # Reset flag since a new highest similarity is found
        elif attribute_similarity == highest_similarity:
            equal_similarity_encountered = True  # Set flag if equal similarity is encountere

        similarities[attribute_name] = attribute_similarity

        print(f"similarity for attribute '{attribute_name}': {attribute_similarity * 100:.2f}%")

    if not equal_similarity_encountered:  # Check if equal similarity is encountered
        if best_attribute:
            print(f"\nThe attribute with the highest similarity is '{best_attribute}' with {highest_similarity * 100:.2f}%.")
        else:
            print("No matching attribute found.")
        print(best_attribute)

    best_attributes = [attr for attr, similarity in similarities.items() if similarity == highest_similarity]

    results=[]
    for best_attribute in best_attributes:
            result = {
                "best_attribute": best_attribute,
                "similarity": highest_similarity*100,
                "matching_features in highest matching": matching_features.get(best_attribute, []),        
            }
            results.append(result)
    output_file = "result.json"  
    with open(output_file, 'w') as outfile:
        json.dump(results, outfile, indent=4)
    return results

def main():
    json1_path = 'groundreality.json'  # Replace with the actual filename
    json2_path = 'received.json'  # Replace with the actual filename
    priority_order = {'shape': 1, 'color': 2, 'letter': 3, 'letter_color': 4}

    json1 = load_json(json1_path)
    json2 = load_json(json2_path)
    
    # Compare features initially
    compare_features(json1, json2,priority_order)
    # print(best_attribute)
    
    # Watch for changes in random.json
    print("Watching random.json for changes...")
    watch_file(json1_path, json2_path, compare_features,priority_order)

def watch_file(json1_path, json2_path, comparison_function,priority_order):
    event_handler = JSONFileChangeHandler(json1_path, json2_path, comparison_function,priority_order)
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
