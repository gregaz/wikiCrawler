
import requests

class WikiArticleRequester:
    """This class is responsible for making requests to the Wiki API to retrieve articles"""

    numberOfHttpRequests = 0
    base_url = 'https://en.wikipedia.org/w/'
    random_article_query_string = 'api.php?action=query&format=json&list=random&rnnamespace=0&rnlimit=NUMBER_OF_ARTICLES_HERE'
    raw_article_query_template = 'index.php?title=TITLE_HERE&action=raw'

    def __generateRawQueryForTitle(self, title):
        return self.raw_article_query_template.replace('TITLE_HERE', title)

    def __makeRequestForQueryString(self, queryString):
        self.numberOfHttpRequests += 1
        return requests.get(self.base_url + queryString)

    def __generateRandomQueryForArticles(self, numberOfArticles):
        return self.random_article_query_string.replace('NUMBER_OF_ARTICLES_HERE', str(numberOfArticles))

    def randomArticleTitle(self):
        return self.getRandomArticleTitles(1)[0]

    def getRawArticle(self, title):
        r = self.__makeRequestForQueryString(self.__generateRawQueryForTitle(title))
        return r.text

    def getRandomArticleTitles(self, numberOfArticles):
        r = self.__makeRequestForQueryString(self.__generateRandomQueryForArticles(numberOfArticles))
        return [each['title'] for each in r.json()['query']['random']]