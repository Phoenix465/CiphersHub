from utils import CiphertextFitnessTracker
import random
import math


alphas = "abcdefghijklmnopqrstuvwxyz".upper()
reverseSubstitute = {a: b for a, b in zip(alphas, alphas[::-1])}
alpha2Nums = {letter: i for i, letter in enumerate(alphas)}
mostCommon = "ETAHONISRDLUGWCFMPYBKVJXQZ"


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

def AffineShift(text, a, b):
    return "".join([alphas[(a*alpha2Nums[char] + b) % 26] for char in text.upper() if char in alphas])

def SubstituteText(text, nAlpha):
    return "".join(nAlpha[alpha2Nums[char]] for char in text)


def RailFenceEncrypt(text, railLength, railOffset, returnList=False, limitRails=True):
    text = "-"*railOffset + "".join([c for c in text.upper() if c in alphas])
    railsRange = list(range(0, railLength))

    rails = [""] * (min(len(text), railLength) if limitRails else railLength)
    rowsOrder = (railsRange + railsRange[-2:0:-1]) * math.ceil(len(text) / max(railLength, 2 * railLength - 2))
    for i, char in enumerate(text):
        if char == "-": continue
        rails[rowsOrder[i]] += char

    return "".join(rails) if not returnList else rails


def RailFenceDecrypt(text, railLength, railOffset):
    # text = [c for c in text.upper() if c in alphas]
    text = list(filter(lambda c: c in alphas, text.upper()))

    length = len(text) + railOffset
    rails = RailFenceEncrypt("X"*length, railLength, 0, returnList=True)

    dummyOffsetsLength = [len(dummy) for dummy in RailFenceEncrypt("X"*railOffset, railLength, 0, returnList=True, limitRails=False)]
    textRails = [["-"]*dummyOffsetsLength[i] + [text.pop(0) for placeholder in row[dummyOffsetsLength[i]:]] for i, row in enumerate(rails)]  # Empties text string

    railsRange = list(range(0, railLength))
    rowsOrder = (railsRange + railsRange[-2:0:-1]) * math.ceil(length / max(railLength, 2 * railLength - 2))

    plainText = [textRails[rowsOrder[i]].pop(0) for i in range(length)]

    return "".join(plainText)[railOffset:]


def CeaserSolver(text, fitnessFunc, num=1):
    tracker = CiphertextFitnessTracker(fitnessFunc=fitnessFunc, resultsTrack=num)

    for i in range(26):
        ctext = CeaserShift(text, -i)
        tracker.add(ctext, metaData={"shift": i})

    return tracker.get()


def VigenereSolver(text, fitnessFunc, num=1):
    tracker = CiphertextFitnessTracker(fitnessFunc=fitnessFunc, resultsTrack=num)

    filterText = "".join([Character for Character in text.upper() if Character in alphas])

    for keyLength in range(1, 50):
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


def AffineSolver(text, fitnessFunc, num=1):
    tracker = CiphertextFitnessTracker(fitnessFunc=fitnessFunc, resultsTrack=num)

    filterText = "".join([Character for Character in text.upper() if Character in alphas])

    A = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]  # Coprime with 26

    for a in A:
        for b in range(26):
            ctext = AffineShift(filterText, a, b)

            # Maps Ctext to text (first two chars)
            map1 = [alpha2Nums[ctext[0]], alpha2Nums[filterText[0]]]
            map2 = [alpha2Nums[ctext[1]], alpha2Nums[filterText[1]]]

            # map1[0]*A + B = map1[1]
            # map1[0]*A + B = map2[1]
            Adiff = map1[0] - map2[0]
            Cdiff = map1[1] - map2[1]

            # Solving Adiff*N - Cdiff = 0 (MOD 26)
            encryptA = "NA"
            encryptB = "NA"
            for i1 in A:
                if (i1*Adiff - Cdiff) % 26 == 0:
                    encryptA = i1

                    for i2 in range(26):
                        if (i1*map1[0]+i2-map1[1]) % 26 == 0:
                            encryptB = i2
                    break
            # Apologises to future self to read this ;(

            tracker.add(ctext, metaData={"a": encryptA, "b": encryptB})

    return tracker.get()


def SubstitutionSolver(text, fitnessFunc, num=5):
    tracker = CiphertextFitnessTracker(fitnessFunc=fitnessFunc, resultsTrack=num)

    fText = "".join([c for c in text.upper() if c in alphas])

    iterations = 10000
    temp = 200
    fitness = -99999
    bestFitness = -99999

    mostCommonCT = "".join(sorted(alphas, key=lambda k: fText.count(k), reverse=True))
    currentAlpha = [mostCommon[mostCommonCT.index(c)] for c in alphas]

    for i in range(iterations):
        swapA = random.randint(0, 25)
        swapB = random.randint(0, 25)

        tempAlpha = currentAlpha.copy()
        tempAlpha[swapA], tempAlpha[swapB] = tempAlpha[swapB], tempAlpha[swapA]

        newText = SubstituteText(fText, tempAlpha)
        newFitness = fitnessFunc(newText)

        T = 1 / (i + 1)
        T2 = T * temp
        prob = math.exp((newFitness - fitness) / T2)
        if newFitness > fitness or random.random() <= prob:
            currentAlpha = tempAlpha
            fitness = newFitness

        if newFitness > bestFitness:
            bestFitness = newFitness

            encryptAlpha = "".join([alphas[tempAlpha.index(c)] for c in alphas])
            tracker.add(newText, fitnessOverride=newFitness, metaData={"key": encryptAlpha})

    return tracker.get()


def RailFenceSolver(text, fitnessFunc, num=5):
    tracker = CiphertextFitnessTracker(fitnessFunc=fitnessFunc, resultsTrack=num)

    for i in range(1, 100):
        if i > len(text):
            break

        for offset in range(2*i):
            # if i == 30 and offset==20:
            #     from line_profiler import LineProfiler
            #     def call(test):
            #         RailFenceDecrypt(text, i, offset)
            #
            #     lp = LineProfiler()
            #     lp.add_function(RailFenceDecrypt)  # add additional function to profile
            #     lp_wrapper = lp(call)
            #     lp_wrapper([i for i in range(100)])
            #     lp.print_stats()

            ctext = RailFenceDecrypt(text, i, offset)
            tracker.add(ctext, metaData={"rail": i, "offset": offset})

    return tracker.get()

