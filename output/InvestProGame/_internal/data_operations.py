import json
import os

DATA_FILE = "game_data.json"
INITIAL_CAPITAL = 100000

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                capital = data.get("capital", INITIAL_CAPITAL)
                investments = data.get("investments", {})
                return capital, investments
        except (json.JSONDecodeError, KeyError) as e:
            print("Error loading data:", e)

    return INITIAL_CAPITAL, {}

def save_data(capital, investments):
    data = {
        "capital": capital,
        "investments": investments
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)