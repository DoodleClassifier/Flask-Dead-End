from flask import Flask, render_template, url_for, send_from_directory, request, jsonify
from flask_bootstrap import Bootstrap
import pickle
import pandas as pd
import logging
# from flask_cors import CORS, cross_origin


# Set flask to only log errors (mostly so that the console isn't spammed with the arrays from prediction route calls)
log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__)
bootstrap = Bootstrap(app)
# cors = CORS(app, resources={r"/DoodleClassifierFlask/*": {"origins": "*"}})

with open("./model.pkl", "rb") as f:
    model = pickle.load(f)

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


@app.route('/predict/<pixels>')
def get_objects(pixels):
    # Split string into array and create df
    data = pixels.split(",")
    df = pd.DataFrame([data])

    # Make predictions
    preds = model.predict_proba(df)
    return {'prediction': preds.tolist()}


if __name__ == '__main__':
    app.run(debug=True)