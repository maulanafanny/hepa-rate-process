from flask import Flask, request
import subprocess

# import pandas as pd
# import numpy as np
# from sklearn.cluster import AgglomerativeClustering
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2

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

if __name__ == "__main__":
    app.run(debug=True)