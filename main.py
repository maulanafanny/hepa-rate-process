from flask import Flask, request, jsonify
import subprocess

import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route("/pull", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = '/home/maulanafanny/process-server'
        process = subprocess.Popen(f'cd {repo} && git pull', stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()

        if process.returncode != 0:
            return {'status': 'failure', 'message': error.decode('utf-8')}, 500
        else:
            return {'status': 'success', 'message': output.decode('utf-8')}, 200
    else:
        return '', 400

@app.route("/clustering", methods=['POST'])
def clustering():
    req = request.get_json()
    df = pd.DataFrame(req['dataset'])

    # clear the console
    # subprocess.call('cls', shell=True)

    features = df[['total_case', 'clean_water_rate', 'safe_house_rate', 'total_population', 'sanitation_rate']]
    scaler = MinMaxScaler(feature_range = (0, 1)).set_output(transform='pandas')
    features = scaler.fit_transform(features)

    # selected_features = features.iloc[:,[0,1,2,3,4]]

    clustering = AgglomerativeClustering(n_clusters=3, linkage='ward')
    clusters = clustering.fit_predict(features)

    data = {
        'cluster': clusters.tolist()
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=3333)