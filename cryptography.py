from utils import CiphertextFitnessTracker


alphas = "abcdefghijklmnopqrstuvwxyz".upper()
reverseSubstitute = {a: b for a, b in zip(alphas, alphas[::-1])}
alpha2Nums = {letter: i for i, letter in enumerate(alphas)}


def frequencyAnalysis(text):
    text = text.upper()

    freq = {c: 0 for c in alphas}
    for letter in text:
        if letter in alphas:
            freq[letter] += 1

    return freq


def IOC(text):
    text = text.upper()

    filterText = "".join([Character for Character in text if Character in alphas])
    ioc = sum(
        [((filterText.count(letter) * (filterText.count(letter) - 1)) / (len(filterText) * (len(filterText) - 1))) for
         letter in alphas])

    return ioc


def Atbash(text):
    return "".join(reverseSubstitute[char] for char in text.upper() if char in alphas)


def CeaserShift(text, shift=0):
    return "".join([alphas[(alpha2Nums[char] + shift) % 26] for char in text.upper() if char in alphas])


def CeaserSolver(text, fitnessFunc, num=1):
    tracker = CiphertextFitnessTracker(fitnessFunc=fitnessFunc, resultsTrack=num)

    for i in range(26):
        ctext = CeaserShift(text, -i)
        tracker.add(ctext, metaData={"shift": i})

    return tracker.get()


def VigenereSolver(text, fitnessFunc, num=1):
    tracker = CiphertextFitnessTracker(fitnessFunc=fitnessFunc, resultsTrack=num)

    filterText = "".join([Character for Character in text.upper() if Character in alphas])

    for keyLength in range(1, 15):
        key = ""

        columns = []

        for i in range(keyLength):
            column = filterText[i::keyLength]
            result = CeaserSolver("".join(column), fitnessFunc, num=1)

            key += alphas[result[0]["metadata"]["shift"]]
            text = result[0]["text"]

            columns.append(text)

        plaintext = "".join([row[i] for i in range(len(columns[0])) for row in columns if i < len(row)])
        tracker.add(plaintext, metaData={"key": key})

    return tracker.get()
