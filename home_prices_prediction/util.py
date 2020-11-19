import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None


def get_estimated_price(_district, _rooms, _size):
    """return a random value to test the request"""
    return 200

    try:
        loc_index = __data_columns.index(suburb.lower())
    except:
        loc_index = -1

    loc_index = np.where(X.columns == suburb)[0][0]

    x = np.zeros(len(X.columns))
    x[0] = rooms
    x[1] = Type
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']

        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open('./artifacts/melbourne_house_price_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved model...done")


def get_location_names():
    """return a random value to test the request"""
    return ['Location 1', 'Location 2']
    return __locations


def get_data_columns():
    return __data_columns


if __name__ == '__main__':
    load_saved_artifacts()