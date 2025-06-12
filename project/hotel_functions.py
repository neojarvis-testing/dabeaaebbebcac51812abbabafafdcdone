import json

# Function to load hotel data from a JSON file
def load_hotels(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save hotel data to a JSON file
def save_hotels(hotels, filename):
    with open(filename, 'w') as file:
        json.dump(hotels, file, indent=4)

