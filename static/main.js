const socket = io();
socket.on('connect', function () {
    console.log("Connected");
});

const cipherTextElement = document.getElementById("CipherTextInput");

const frequencyLetterTemplate = document.querySelector("#FrequencyLetterTemplate");
const frequencyNumberTemplate = document.querySelector("#FrequencyNumberTemplate");
const ceaserOutputTemplate = document.querySelector("#CeaserOutputTemplate");

const frequencyLetters = document.getElementById("FrequencyLetters");
const frequencyValue = document.getElementById("FrequencyValue");
const frequencyPercentage = document.getElementById("FrequencyPercentage");

const IOCValue = document.getElementById("IOCValue");

const AtbashPT = document.getElementById("AtbashPT");
const AtbashInfo = document.getElementById("AtbashInfo");

const CeaserOutputs = document.getElementById("CeaserOutputs");
const VigenereOutputs = document.getElementById("VigenereOutputs");

const FrequencyAnalysisStatus = document.getElementById("FrequencyAnalysisStatus")
const IOCStatus = document.getElementById("IOCStatus")
const AtbashStatus = document.getElementById("AtbashStatus")
const CeaserStatus = document.getElementById("CeaserStatus")
const VigenereStatus = document.getElementById("VigenereStatus")

const topResultsNumber = 5;

const sumValues = obj => Object.values(obj).reduce((a, b) => a + b, 0);


function autoGrowTextArea(element) {
    element.style.height = "5px";
    element.style.height = element.scrollHeight + "px";
}

function round(num, digits) {
    return Math.round(num * Math.pow(10, digits)) / Math.pow(10, digits);
}

function setStatus(element, isBusy) {
    if (isBusy === true) {
        element.innerText = "BUSY"
        element.classList.add("red")
        element.classList.remove("green")
    } else {
        element.innerText = "READY"
        element.classList.add("green")
        element.classList.remove("red")
    }


}

function reset() {
    applyFrequencyAnalysis(
    ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
    {"A":0,"B":0,"C":0,"D":0,"E":0,"F":0,"G":0,"H":0,"I":0,"J":0,"K":0,"L":0,"M":0,"N":0,"O":0,"P":0,"Q":0,"R":0,"S":0,"T":0,"U":0,"V":0,"W":0,"X":0,"Y":0,"Z":0}
    );
    applyIOC(0);
    applyAtbash("", 0, "NA");
    CeaserOutputs.innerHTML = "";
    applyCeaser("", "NA", "NA", "Fitness");
    VigenereOutputs.innerHTML = "";
    applyVigenere("", "NA", "NA", "Fitness");
}

function compute() {
    const text = cipherTextElement.value;

    reset()

    setStatus(FrequencyAnalysisStatus, true);
    setStatus(IOCStatus, true);
    setStatus(AtbashStatus, true);
    setStatus(CeaserStatus, true);
    setStatus(VigenereStatus, true);

    socket.emit("requestFrequencyAnalysis", {ctext: text});
    socket.emit("requestIOC", {ctext: text});
    socket.emit("requestAtbash", {ctext: text});
    socket.emit("requestCeaser", {ctext: text});
    socket.emit("requestVigenere", {ctext: text});
}
function applyFrequencyAnalysis(keysSort, frequency) {
    frequencyLetters.innerHTML = ""
    frequencyValue.innerHTML = "";
    frequencyPercentage.innerHTML = "";

    let sumFreq = sumValues(frequency);

    for(let i = 0; i < keysSort.length; i++) {
        let letter = keysSort[i];

        let letterClone = frequencyLetterTemplate.innerHTML;
        letterClone = letterClone.replaceAll("--", letter);

        let frequencyClone = frequencyNumberTemplate.innerHTML;
        frequencyClone = frequencyClone.replaceAll("--", frequency[letter]);

        let percentageClone = frequencyNumberTemplate.innerHTML;
        percentageClone = percentageClone.replaceAll("--", sumFreq === 0 ? "0%" : `${Math.round(frequency[letter]/sumFreq*1000)/10}%`);


        frequencyLetters.insertAdjacentHTML("beforeend", letterClone);
        frequencyValue.insertAdjacentHTML("beforeend", frequencyClone);
        frequencyPercentage.insertAdjacentHTML("beforeend", percentageClone);
    }

    setStatus(FrequencyAnalysisStatus, false);
}

function applyIOC(ioc) {
    IOCValue.innerText = `${round(ioc, 6)}`

    setStatus(IOCStatus, false);
}

function applyAtbash(text, fitness, fitnessName) {
    AtbashPT.value = text;
    AtbashInfo.innerText = `${fitnessName}: ${round(fitness, 6)}`
    autoGrowTextArea(AtbashPT);

    setStatus(AtbashStatus, false);
}

function applyCeaser(text, shift, fitness, fitnessName) {
    let ceaserOutput = ceaserOutputTemplate.content.cloneNode(true);
    let ceaserPT = ceaserOutput.querySelector(".TextInputSmall");
    ceaserPT.value = text;

    let ceaserInfo = ceaserOutput.querySelector(".CeaserInfo");

    ceaserInfo.innerHTML = `${fitnessName}: ${round(fitness, 6)}<br>Shift: ${shift}`;
    CeaserOutputs.appendChild(ceaserOutput);
    autoGrowTextArea(ceaserPT);

    setStatus(CeaserStatus, false);
}

function applyVigenere(text, key, fitness, fitnessName) {
    let vigenereOutput = ceaserOutputTemplate.content.cloneNode(true);
    let vigenerePT = vigenereOutput.querySelector(".TextInputSmall");
    vigenerePT.value = text;

    let vigenereInfo = vigenereOutput.querySelector(".CeaserInfo");

    vigenereInfo.innerHTML = `${fitnessName}: ${round(fitness, 6)}<br>Key: ${key}`;
    VigenereOutputs.appendChild(vigenereOutput);
    autoGrowTextArea(vigenerePT);

    setStatus(VigenereStatus, false);
}

socket.on("result", function (data) {
    const resultType = data.type;
    const result = data["result"];

    console.log(data);
    // document.getElementById(resultType).innerText = JSON.stringify(result);

    if (resultType === "FrequencyAnalysis") {
        const keysSort = result["keysSort"];
        const frequency = result["frequency"];

        applyFrequencyAnalysis(keysSort, frequency);
    }
    else if (resultType === "IOC") {
        const ioc = result["ioc"];

        applyIOC(ioc);
    }
    else if (resultType === "Atbash") {
        const plaintext = result["plaintext"];
        const fitness = result["fitness"];
        const fitnessName = result["fitnessName"];

        applyAtbash(plaintext, fitness, fitnessName);
    }
    else if (resultType === "Ceaser") {
        CeaserOutputs.innerHTML = "";
        for(let i = 0; i < result.length; i++) {
            const fitness = result[i]["fitness"];
            const text = result[i]["text"];
            const shift = result[i]["metadata"]["shift"];

            applyCeaser(text, shift, fitness, data["fitnessName"]);
        }
    }
    else if (resultType === "Vigenere") {
        VigenereOutputs.innerHTML = "";
        for(let i = 0; i < result.length; i++) {
            const fitness = result[i]["fitness"];
            const text = result[i]["text"];
            const key = result[i]["metadata"]["key"];

            applyVigenere(text, key, fitness, data["fitnessName"]);
        }
    }
})

reset();