def profile(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        from line_profiler import LineProfiler
        prof = LineProfiler()
        try:
            return prof(func)(*args, **kwargs)
        finally:
            prof.print_stats()

    return wrapper


class CiphertextFitnessTracker:
    def __init__(self, fitnessFunc, resultsTrack: int = 1):
        self.fitnessFunc = fitnessFunc
        self.resultsTrack = resultsTrack

        self.fitnesses = []
        self.texts = []
        self.metaData = []
        self.minFitness = None

    def add(self, text, fitnessOverride=None, metaData=None):
        fitness = fitnessOverride or self.fitnessFunc(text)

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
