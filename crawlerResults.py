from itertools import groupby

class CrawlerResult:
    title = ''
    path = []

    def __init__(self, title, path):
        self.title = title
        self.path = path

class CrawlerResults:
    results = []

    def add(self,aResult):
        self.results.append(aResult)

    def printResultStats(self):
        numberOfFailedPaths = 0
        sucessfulPaths = []
        numberOfArticles = len(self.results)

        for result in self.results:
            if result.path is None:
                numberOfFailedPaths += 1
            else:
                sucessfulPaths.append(result.path)

        distributionDict = {}
        for length,group in groupby(sucessfulPaths, lambda x: len(x)):
            distributionDict[length] = len(list(group))

        if len(sucessfulPaths) != 0:
            averageSuccessfulPathLength = sum([len(each) for each in sucessfulPaths]) / len(sucessfulPaths)
        else:
            averageSuccessfulPathLength = 0
        numberOfSuccessfulPaths = len(sucessfulPaths)

        print('Number of paths tried: ' + str(numberOfArticles))
        print('Number of successful paths: ' + str(numberOfSuccessfulPaths))
        print('Number of failed paths: ' + str(numberOfFailedPaths))
        print('Percentage of successful paths: ' + "%.5f%%" % (100.0 * float(numberOfSuccessfulPaths) / float(numberOfArticles)))
        print('Average successful path length: ' + str(averageSuccessfulPathLength))

        print('Distribution: ' + str(distributionDict))


