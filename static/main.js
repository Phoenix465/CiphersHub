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
const AffineOutputs = document.getElementById("AffineOutputs");
const SubstitutionOutputs = document.getElementById("SubstitutionOutputs");
const RailFenceOutputs = document.getElementById("RailFenceOutputs");

const FrequencyAnalysisStatus = document.getElementById("FrequencyAnalysisStatus")
const IOCStatus = document.getElementById("IOCStatus")
const AtbashStatus = document.getElementById("AtbashStatus")
const CeaserStatus = document.getElementById("CeaserStatus")
const VigenereStatus = document.getElementById("VigenereStatus")
const AffineStatus = document.getElementById("AffineStatus")
const SubstitutionStatus = document.getElementById("SubstitutionStatus")
const RailFenceStatus = document.getElementById("RailFenceStatus")

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

    applyAtbash("", 0, "Fitness");

    CeaserOutputs.innerHTML = "";
    applyCeaser("", "NA", "NA", "Fitness");

    VigenereOutputs.innerHTML = "";
    applyVigenere("", "NA", "NA", "Fitness");

    AffineOutputs.innerHTML = "";
    applyAffine("", "NA", "NA", "NA", "Fitness");

    SubstitutionOutputs.innerHTML = "";
    applySubstitution("", "NA", "NA", "Fitness");

    RailFenceOutputs.innerHTML = "";
    applyRailFence("", "NA", "NA", "Fitness");
}

function compute() {
    const text = cipherTextElement.value;

    reset()

    setStatus(FrequencyAnalysisStatus, true);
    setStatus(IOCStatus, true);
    setStatus(AtbashStatus, true);
    setStatus(CeaserStatus, true);
    setStatus(VigenereStatus, true);
    setStatus(AffineStatus, true);
    setStatus(SubstitutionStatus, true);
    setStatus(RailFenceStatus, true);

    socket.emit("requestFrequencyAnalysis", {ctext: text});
    socket.emit("requestIOC", {ctext: text});
    socket.emit("requestAtbash", {ctext: text});
    socket.emit("requestCeaser", {ctext: text});
    socket.emit("requestVigenere", {ctext: text});
    socket.emit("requestAffine", {ctext: text});
    socket.emit("requestSubstitution", {ctext: text});
    socket.emit("requestRailFence", {ctext: text});
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

    if (CeaserOutputs.dataset.hide === "true") {
        ceaserPT.classList.add("HideExtraSiblings")
        let lastChild = CeaserOutputs.lastElementChild;
        lastChild.classList.add("HideExtraSiblings")
    }

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

    if (VigenereOutputs.dataset.hide === "true") {
        vigenerePT.classList.add("HideExtraSiblings")
        let lastChild = VigenereOutputs.lastElementChild;
        lastChild.classList.add("HideExtraSiblings")
    }


    setStatus(VigenereStatus, false);
}


function applyAffine(text, a, b, fitness, fitnessName) {
    let affineOutput = ceaserOutputTemplate.content.cloneNode(true);
    let affinePT = affineOutput.querySelector(".TextInputSmall");
    affinePT.value = text;

    let affineInfo = affineOutput.querySelector(".CeaserInfo");

    affineInfo.innerHTML = `${fitnessName}: ${round(fitness, 6)}<br>A: ${a} | B: ${b}`;
    AffineOutputs.appendChild(affineOutput);
    autoGrowTextArea(affinePT);

    if (AffineOutputs.dataset.hide === "true") {
        affinePT.classList.add("HideExtraSiblings")
        let lastChild = AffineOutputs.lastElementChild;
        lastChild.classList.add("HideExtraSiblings")
    }

    setStatus(AffineStatus, false);
}


function applySubstitution(text, key, fitness, fitnessName) {
    let substitutionOutput = ceaserOutputTemplate.content.cloneNode(true);
    let substitutionPT = substitutionOutput.querySelector(".TextInputSmall");
    substitutionPT.value = text;

    let substitutionInfo = substitutionOutput.querySelector(".CeaserInfo");

    substitutionInfo.innerHTML = `${fitnessName}: ${round(fitness, 6)}<br>Key: ${key}`;
    SubstitutionOutputs.appendChild(substitutionOutput);
    autoGrowTextArea(substitutionPT);

    if (SubstitutionOutputs.dataset.hide === "true") {
        substitutionPT.classList.add("HideExtraSiblings")
        let lastChild = SubstitutionOutputs.lastElementChild;
        lastChild.classList.add("HideExtraSiblings")
    }

    setStatus(SubstitutionStatus, false);
}


function applyRailFence(text, rails, fitness, fitnessName) {
    let railFenceOutput = ceaserOutputTemplate.content.cloneNode(true);
    let railFencePT = railFenceOutput.querySelector(".TextInputSmall");
    railFencePT.value = text;

    let railFenceInfo = railFenceOutput.querySelector(".CeaserInfo");

    railFenceInfo.innerHTML = `${fitnessName}: ${round(fitness, 6)}<br>Rails: ${rails}`;
    RailFenceOutputs.appendChild(railFenceOutput);
    autoGrowTextArea(railFencePT);

    if (RailFenceOutputs.dataset.hide === "true") {
        railFencePT.classList.add("HideExtraSiblings")
        let lastChild = RailFenceOutputs.lastElementChild;
        lastChild.classList.add("HideExtraSiblings")
    }

    setStatus(RailFenceStatus, false);
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
    else if (resultType === "Affine") {
        AffineOutputs.innerHTML = "";
        for(let i = 0; i < result.length; i++) {
            const fitness = result[i]["fitness"];
            const text = result[i]["text"];
            const a = result[i]["metadata"]["a"];
            const b = result[i]["metadata"]["b"];

            applyAffine(text, a, b, fitness, data["fitnessName"]);
        }
    }
    else if (resultType === "Substitution") {
        SubstitutionOutputs.innerHTML = "";
        for(let i = 0; i < result.length; i++) {
            const fitness = result[i]["fitness"];
            const text = result[i]["text"];
            const key = result[i]["metadata"]["key"];

            applySubstitution(text, key, fitness, data["fitnessName"]);
        }
    }
    else if (resultType === "RailFence") {
        RailFenceOutputs.innerHTML = "";
        for(let i = 0; i < result.length; i++) {
            const fitness = result[i]["fitness"];
            const text = result[i]["text"];
            const rail = result[i]["metadata"]["rail"];

            applyRailFence(text, rail, fitness, data["fitnessName"]);
        }
    }
})

function expandButtonClick(buttonElement, outputId) {
    let outputElement = document.getElementById(outputId)
    let hide = outputElement.dataset.hide === "true";
    outputElement.dataset.hide = hide ? "false" : "true";

    buttonElement.innerText = !hide ? "+" : "-";

    let outputChildren = outputElement.children;
    for(const child of outputChildren) {
        if (!hide) {
            child.classList.add("HideExtraSiblings");
        } else {
            child.classList.remove("HideExtraSiblings");
        }
    }
}

reset();

var allExpandButtons = document.querySelectorAll('div[class^=CipherExpand]');