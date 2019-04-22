import glob
import json
from common.levenshtein import lev_biased


# load items from data into dictionary, using item name as key
def load_items():
    items = {}
    folder = 'data/items/'
    for filename in glob.glob(folder + '*.json'):
        with open(filename, 'r') as f:
            data = json.load(f)
            for item in data:
                items[item['name']] = item
    print("{} items loaded from file".format(len(items)))
    return items


# get closest match from items list, return item and similarity score
def get_item(item_name, items):
    def dist(x): return lev_biased(item_name, x, 10, 1, 10)
    best_guess = min(items.keys(), key=lambda x: dist(x))
    return best_guess, dist(best_guess)