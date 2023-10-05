from flask import Flask, render_template
from flask_socketio import send, emit, SocketIO
import logging
from os import path, walk

import analysis
import cryptography
import ngram_score

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app)

fitnessFuncName = "Quadgrams Log"
fitnessFunc = ngram_score.ngram_score("english_quadgrams.txt").score


@app.route("/")
def home():
   return render_template('index.html')


@socketio.on("connect")
def connectedClient(data):
    print(f'Client Connected {data  }')


@socketio.on("requestFrequencyAnalysis")
def requestFrequencyAnalysis(data):
    if "ctext" in data:
        text = data["ctext"]
        freq = cryptography.frequencyAnalysis(text)

        emit("result", {
            "type": "FrequencyAnalysis",
            "result": {
                "frequency": freq,
                "keysSort": list(sorted(freq.keys(), key=lambda k: -freq[k]))
            }
        })

@socketio.on("requestIOC")
def requestIOC(data):
    if "ctext" in data:
        text = data["ctext"]
        ioc = cryptography.IOC(text)

        emit("result", {
            "type": "IOC",
            "result": {
                "ioc": ioc,
            }
        })


@socketio.on("requestAtbash")
def requestAtbash(data):
    if "ctext" in data:
        text = data["ctext"]
        pText = cryptography.Atbash(text)
        fitness = fitnessFunc(pText)

        emit("result", {
            "type": "Atbash",
            "result": {
                "plaintext": pText,
                "fitness": fitness,
                "fitnessName": fitnessFuncName,
            }
        })


@socketio.on("requestCeaser")
def requestAtbash(data):
    if "ctext" in data:
        text = data["ctext"]
        results = cryptography.CeaserSolver(text, fitnessFunc=fitnessFunc, num=5)

        emit("result", {
            "type": "Ceaser",
            "result": results,
            "fitnessName": fitnessFuncName,
        })


@socketio.on("requestVigenere")
def requestVigenere(data):
    if "ctext" in data:
        text = data["ctext"]

        results = cryptography.VigenereSolver(text, fitnessFunc=fitnessFunc, num=5)

        emit("result", {
            "type": "Vigenere",
            "result": results,
            "fitnessName": fitnessFuncName,
        })


@socketio.on("requestAffine")
def requestAffine(data):
    if "ctext" in data:
        text = data["ctext"]

        if len(text) <=2:
            emit("result", {
                "type": "Affine",
                "result": [],
                "fitnessName": fitnessFuncName,
            })

        results = cryptography.AffineSolver(text, fitnessFunc=fitnessFunc, num=5)

        emit("result", {
            "type": "Affine",
            "result": results,
            "fitnessName": fitnessFuncName,
        })


@socketio.on("requestSubstitution")
def requestSubstitution(data):
    if "ctext" in data:
        text = data["ctext"]

        results = cryptography.SubstitutionSolver(text, fitnessFunc=fitnessFunc, num=5)

        emit("result", {
            "type": "Substitution",
            "result": results,
            "fitnessName": fitnessFuncName,
        })


@socketio.on("requestRailFence")
def requestRailFence(data):
    if "ctext" in data:
        text = data["ctext"]
        results = cryptography.RailFenceSolver(text, fitnessFunc=fitnessFunc, num=5)

        emit("result", {
            "type": "RailFence",
            "result": results,
            "fitnessName": fitnessFuncName,
        })


@socketio.on("requestColumnTransposition")
def requestColumnTransposition(data):
    if "ctext" in data:
        text = data["ctext"]
        results = cryptography.ColumnTranspositionWRWC(text, fitnessFunc=fitnessFunc, num=5)

        emit("result", {
            "type": "ColumnTransposition",
            "result": results,
            "fitnessName": fitnessFuncName,
        })


if __name__ == "__main__":
    extraDirs = [r'.\static', r'.\templates']
    extraFiles = extraDirs[:]
    for extraDir in extraDirs:
        for dirname, dirs, files in walk(extraDir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extraFiles.append(filename)
    print(extraFiles)

    socketio.run(app=app, debug=True, use_reloader=True, allow_unsafe_werkzeug=True, extra_files=extraFiles)
    # socketio.run(host="0.0.0.0", app=app, debug=True, use_reloader=True, allow_unsafe_werkzeug=True, extra_files=extraFiles)
