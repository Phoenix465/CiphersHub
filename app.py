from flask import Flask, render_template
from flask_socketio import send, emit, SocketIO
import logging
from os import path, walk

import analysis
import cryptography


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app)

fitnessFuncName = "PMCC Bigrams"
fitnessFunc = analysis.pmcc_b


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
        print(results)
        emit("result", {
            "type": "Ceaser",
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
