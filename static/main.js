const socket = io();
socket.on('connect', function () {
    console.log("Connected");
});

const cipherTextElement = document.getElementById("CipherTextInput");

const frequencyLetterTemplate = document.querySelector("#FrequencyLetterTemplate");
const frequencyNumberTemplate = document.querySelector("#FrequencyNumberTemplate");
const CipherMultipleOutputTemplate = document.querySelector("#CipherMultipleOutputTemplate");

const frequencyLetters = document.getElementById("FrequencyLetters");
const frequencyValue = document.getElementById("FrequencyValue");
const frequencyPercentage = document.getElementById("FrequencyPercentage");

const IOCValue = document.getElementById("IOCValue");

const AtbashPT = document.getElementById("AtbashPT");
const AtbashInfo = document.getElementById("AtbashInfo");

const FrequencyAnalysisStatus = document.getElementById("FrequencyAnalysisStatus")

const topResultsNumber = 5;

const sumValues = obj => Object.values(obj).reduce((a, b) => a + b, 0);


function autoGrowTextArea(element) {
    element.style.height = "5px";
    element.style.height = element.scrollHeight + "px";
}

function round(num, digits) {
    return Math.round(num * Math.pow(10, digits)) / Math.pow(10, digits);
}

function setStatus(cipherType, isBusy) {
    let element = document.getElementById(`${cipherType}Status`)
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

function resetOutput(cipherType) {
    let element = document.getElementById(`${cipherType}Outputs`)
    element.innerHTML = "";
}

function reset() {
    applyFrequencyAnalysis(
    ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"],
    {"A":0,"B":0,"C":0,"D":0,"E":0,"F":0,"G":0,"H":0,"I":0,"J":0,"K":0,"L":0,"M":0,"N":0,"O":0,"P":0,"Q":0,"R":0,"S":0,"T":0,"U":0,"V":0,"W":0,"X":0,"Y":0,"Z":0}
    );
    applyIOC(0);

    applyAtbash("", 0, "Fitness");

    resetOutput("Ceaser");
    resetOutput("Vigenere");
    resetOutput("Affine");
    resetOutput("Substitution");
    resetOutput("RailFence");

    applyMultipleCiphersOutput("Ceaser", "", [`Fitness: NA`, `Shift: NA`])
    applyMultipleCiphersOutput("Vigenere", "", [`Fitness: NA`, `Key: NA`])
    applyMultipleCiphersOutput("Affine", "", [`Fitness: NA`, `A: NA | B: NA`])
    applyMultipleCiphersOutput("Substitution", "", [`Fitness: NA`, `Key: NA`])
    applyMultipleCiphersOutput("RailFence", "", [`Fitness: NA`, `Rails: NA`])
}

function compute() {
    const text = cipherTextElement.value;

    reset()

    setStatus("FrequencyAnalysis", true);
    setStatus("IOC", true);
    setStatus("Atbash", true);
    setStatus("Ceaser", true);
    setStatus("Vigenere", true);
    setStatus("Affine", true);
    setStatus("Substitution", true);
    setStatus("RailFence", true);

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

    setStatus("FrequencyAnalysis", false);
}

function applyIOC(ioc) {
    IOCValue.innerText = `${round(ioc, 6)}`

    setStatus("IOC", false);
}

function applyAtbash(text, fitness, fitnessName) {
    AtbashPT.value = text;
    AtbashInfo.innerText = `${fitnessName}: ${round(fitness, 6)}`
    autoGrowTextArea(AtbashPT);

    setStatus("Atbash", false);
}


function applyMultipleCiphersOutput(cipherType, text, metaStringList) {
    let CipherOutputs = document.getElementById(`${cipherType}Outputs`);

    let cipherOutput = CipherMultipleOutputTemplate.content.cloneNode(true);

    let cipherPT = cipherOutput.querySelector(".TextInputSmall");
    cipherPT.value = text;

    let cipherInfo = cipherOutput.querySelector(".CipherInfo");

    cipherInfo.innerHTML = metaStringList.join("<br>");
    CipherOutputs.appendChild(cipherOutput);
    autoGrowTextArea(cipherPT);

    if (CipherOutputs.dataset.hide === "true") {
        cipherPT.classList.add("HideExtraSiblings")
        let lastChild = CipherOutputs.lastElementChild;
        lastChild.classList.add("HideExtraSiblings")
    }

    setStatus(cipherType, false);
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
            const fitness = round(result[i]["fitness"], 6);
            const text = result[i]["text"];
            const shift = result[i]["metadata"]["shift"];

            let metaDataList = [`${data["fitnessName"]}: ${fitness}`, `Shift: ${shift}`]
            applyMultipleCiphersOutput("Ceaser", text, metaDataList)
        }
    }
    else if (resultType === "Vigenere") {
        VigenereOutputs.innerHTML = "";
        for(let i = 0; i < result.length; i++) {
            const fitness = round(result[i]["fitness"], 6);
            const text = result[i]["text"];
            const key = result[i]["metadata"]["key"];

            let metaDataList = [`${data["fitnessName"]}: ${fitness}`, `Key: ${key}`]
            applyMultipleCiphersOutput("Vigenere", text, metaDataList)
        }
    }
    else if (resultType === "Affine") {
        AffineOutputs.innerHTML = "";
        for(let i = 0; i < result.length; i++) {
            const fitness = round(result[i]["fitness"], 6);
            const text = result[i]["text"];
            const a = result[i]["metadata"]["a"];
            const b = result[i]["metadata"]["b"];

            let metaDataList = [`${data["fitnessName"]}: ${fitness}`, `A: ${a} | B: ${b}`]
            applyMultipleCiphersOutput("Affine", text, metaDataList)
        }
    }
    else if (resultType === "Substitution") {
        SubstitutionOutputs.innerHTML = "";
        for(let i = 0; i < result.length; i++) {
            const fitness = round(result[i]["fitness"], 6);
            const text = result[i]["text"];
            const key = result[i]["metadata"]["key"];

            let metaDataList = [`${data["fitnessName"]}: ${fitness}`, `Key: ${key}`]
            applyMultipleCiphersOutput("Substitution", text, metaDataList)
        }
    }
    else if (resultType === "RailFence") {
        RailFenceOutputs.innerHTML = "";
        for(let i = 0; i < result.length; i++) {
            const fitness = round(result[i]["fitness"], 6);
            const text = result[i]["text"];
            const rail = result[i]["metadata"]["rail"];
            const offset = result[i]["metadata"]["offset"];

            let metaDataList = [`${data["fitnessName"]}: ${fitness}`, `Rails: ${rail} | Offset: ${offset}`]
            applyMultipleCiphersOutput("RailFence", text, metaDataList)
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