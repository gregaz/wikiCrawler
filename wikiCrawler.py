#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4

from wikiArticleRequester import WikiArticleRequester
from wikiPageParser import WikiPageParser
from crawlerResults import CrawlerResult, CrawlerResults
import sys


class WikiCrawler:
    pathCache = {}
    requester = WikiArticleRequester()
    parser = WikiPageParser()

    def inefficientFindXPathsFromRandomArticles(self, numberOfArticles):
        results = CrawlerResults()
        for i in range(numberOfArticles):
            results.add(crawler.findPathToPhilosophyFromRandomArticle())

        return results

    def findPathToPhilosophyFromRandomArticle(self):
        randomTitle = self.requester.randomArticleTitle()
        path = []
        pathSet = set()
        path.append(randomTitle)
        pathSet.add(randomTitle)

        while path[-1].lower() != 'philosophy':
            rawArticle = self.requester.getRawArticle(path[-1])
            firstLink = self.parser.getFirstLegitimateLinkTitleForString(rawArticle)
            #if there is no link on article, we hit a dead end
            if firstLink is None:
                print('No First Link')
                print(path)
                return CrawlerResult(randomTitle, None)
            path.append(firstLink)
            #if we see the same article twice, we've hit an infinite loop
            if firstLink in pathSet:
                print('We hit a loop in: ')
                print(path)
                return CrawlerResult(randomTitle, None)
            else:
                pathSet.add(firstLink)
        print('success!')
        print(path)
        return CrawlerResult(randomTitle, path)

    def findPathToPhilosophyFromRandomArticles(self, numberOfArticles):
        randomTitles = self.requester.getRandomArticleTitles(numberOfArticles)
        successfulPathsDict = {}
        failedPathSet = set()
        results = CrawlerResults()

        for randomTitle in randomTitles:
            path = []
            pathSet = set()
            path.append(randomTitle)
            pathSet.add(randomTitle)

            while True:
                if path[-1].lower() == 'philosophy':
                    print('success for: ' + str(path))
                    results.add(CrawlerResult(randomTitle, path))
                    for i,each in enumerate(path):
                        successfulPathsDict[each.lower()] = [each.lower() for each in path[i:]]
                    break

                elif path[-1].lower() in failedPathSet:
                    print(randomTitle + ' failed based off cache: ' + str(path))
                    results.add(CrawlerResult(randomTitle, None))
                    break

                elif path[-1].lower() in successfulPathsDict.keys():
                    path.extend(successfulPathsDict[path[-1].lower()][1:])
                    results.add(CrawlerResult(randomTitle, path))
                    print(randomTitle + ' success based off cache: ' + str(path))
                    break

                else:
                    rawArticle = self.requester.getRawArticle(path[-1])
                    nextLink = self.parser.getFirstLegitimateLinkTitleForString(rawArticle)

                    if nextLink is None:
                        print('Dead end for:' + str(path))
                        results.add(CrawlerResult(randomTitle, None))
                        for each in path:
                            failedPathSet.add(each.lower())
                        break

                    elif nextLink in pathSet:
                        path.append(nextLink)
                        print('We hit a loop in: ' + str(path))
                        results.add(CrawlerResult(randomTitle, None))
                        for each in path:
                            failedPathSet.add(each.lower())
                        break
                    else:
                        path.append(nextLink)
                        pathSet.add(nextLink)

        return results


crawler = WikiCrawler()
crawlResults = crawler.findPathToPhilosophyFromRandomArticles(int(sys.argv[1]))
crawlResults.printResultStats()
print('Number of HTTP requests: ' + str(crawler.requester.numberOfHttpRequests))
