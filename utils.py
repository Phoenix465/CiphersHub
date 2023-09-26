class CiphertextFitnessTracker:
    def __init__(self, fitnessFunc, resultsTrack: int = 1):
        self.fitnessFunc = fitnessFunc
        self.resultsTrack = resultsTrack

        self.fitnesses = []
        self.texts = []
        self.metaData = []
        self.minFitness = None

    def add(self, text, metaData=None):
        fitness = self.fitnessFunc(text)

        if self.minFitness is None or len(self.fitnesses) < self.resultsTrack:
            self.fitnesses.append(fitness)

            self.texts.append(text)
            self.metaData.append(metaData or {})
            self.minFitness = min(self.fitnesses)

        elif fitness > self.minFitness:
            indexRemove = self.fitnesses.index(self.minFitness)
            del self.fitnesses[indexRemove]
            del self.texts[indexRemove]
            del self.metaData[indexRemove]

            self.fitnesses.append(fitness)
            self.texts.append(text)
            self.metaData.append(metaData or {})
            self.minFitness = min(self.fitnesses)

    def get(self):
        fitnessIndexSorted = sorted(range(len(self.fitnesses)), key=lambda i: self.fitnesses[i], reverse=True)
        return [{"fitness": self.fitnesses[fitIndex], "text": self.texts[fitIndex], "metadata": self.metaData[fitIndex]} for fitIndex in fitnessIndexSorted]


