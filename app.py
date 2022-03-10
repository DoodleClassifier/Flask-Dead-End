from flask import Flask, render_template, url_for, send_from_directory, request, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/test', methods=['GET', 'POST'])
# def testfn():
#     # Get request
#     if request.method == 'GET':
#         message = {'greeting': 'Hello from Flask app.py! 2'}
#         return jsonify(message) # Serialize and use JSON headers

#     # Post request
#     if request.method == 'POST':
#         print(request.get_json()) # Parse as JSON
#         return 'Success', 200


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)



from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
import numpy as np
import pandas as pd
from os.path import exists
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

objects = {
    0: "Bowtie",
    1: "Broom",
    2: "Crown",
    3: "EiffelTower",
    4: "HotAirBalloon",
    5: "HousePlant",
    6: "Bed",
    7: "Cat",
    8: "Couch",
    9: "Dog",
    10: "Hand",
    11: "Hat",
    12: "Tractor"
}

data = pd.DataFrame()

# Load data from all npy files
for object in objects:

    # Load the numpy file
    object_data = None
    if exists(f"./data/{objects[object]}.npy"):
        object_data = np.load(f"./data/{objects[object]}.npy")
    else:
        object_data = np.load(
            f"./DoodleClassifierModel/data/{objects[object]}.npy")

    # Add labels to data
    temp = pd.DataFrame(object_data)
    temp["Label"] = object

    # Append object data to main dataframe
    data = pd.concat([data, temp], ignore_index=True)

print("Loaded data...")


# Train test validation split
x_train, x_test, y_train, y_test = train_test_split(
    data.loc[:, data.columns != "Label"], data["Label"], test_size=0.33, random_state=69)

print("Created train test split...")


model = RFC(n_estimators=100, max_depth=None, random_state=420)

print("Created model...")

model.fit(x_train, y_train)

print("trained model...")

def make_prediction(pred):
    """Makes a prediction using the model, takes in a pandas series, aka a single row from a pandas df, or an array of the pixel values"""
    return model.predict_proba(pred)

# @app.route('/train-model', methods=['GET', 'POST'])
# def train_model():
#     model.fit(x_train, y_train)

#     # TODO: Remove this get request? Is it necessary? How does it work?

#     # Get request
#     if request.method == 'GET':
#         message = {'message': 'none'}
#         return jsonify(message) # Serialize and use JSON headers

#     # Post request
#     if request.method == 'POST':
#         print(request.get_json()) # Parse as JSON
#         return 'Success', 200

@app.route('/test-model', methods=['GET', 'POST'])
def test_model():

    test_prediction = make_prediction([data.iloc[2001].drop("Label")]).tolist()

    # Get request
    if request.method == 'GET':
        message = {'prediction': test_prediction}
        return jsonify(message) # Serialize and use JSON headers

    # Post request
    if request.method == 'POST':
        print(request.get_json()) # Parse as JSON
        return 'Success', 200

@app.route('/get-objects', methods=['GET', 'POST'])
def get_objects():
    # Get request
    if request.method == 'GET':
        message = {'objects': objects}
        return jsonify(message) # Serialize and use JSON headers

    # Post request
    if request.method == 'POST':
        print(request.get_json()) # Parse as JSON
        return 'Success', 200


if __name__ == '__main__':
    app.run(debug=True)