**Basic Wiki Crawler**
=======================

If you take a random article from Wikipedia, and follow the first link in the article, how long will it take for you to reach the Philosophy page?

How to Run
----------
Steps to run:

 1. You will need to have python3.4 installed (I chose 3.4 because that is the newest version supported by requests, the http request library I used).
 2. You will need to install requests, which you can do using pip running the command: `python3.4 -m pip install requests`
 3. Change the first line in wikiCrawler.py to your specific python3.4 path if necessary. 
 4. Then you should be able to run the script via the command line as follows:

    ./wikiCrawler.py 500

or

    python3.4 wikiCrawler.py 500

where 500 is the number of random articles to search for

Results
-----------
**Summary:**
Number of paths tried: 500
Number of successful paths: 463
Number of failed paths: 37
Percentage of successful paths: 92.60000%
Average successful path length: 18.29157667386609
Distribution: {3: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 3, 20: 2, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 31: 1, 32: 1, 33: 1, 36: 1, 37: 1, 38: 1, 39: 1}
Number of HTTP requests: 4485
Results from one run stored in 500results.txt

Distribution is a dictionary where the path length to philosophy is the key and number of starting articles with that path length is the value.

The percentage is surprisingly high, but after thinking about it, it makes perfect sense. The first link in an article is usually a more generic type of article. For example, the article for a person usually starts off as "Albert Einstein was a **theoretical physicist**", or "New York is a **state**". Each first link gets more and more generic until you reach the very overarching/generic topic of philosophy.


Reducing Number of HTTP Requests
--------------------------------

 - Caching the path for each step reduces the number of HTTP requests. I.e. if you have one path that goes from A->B->C->Philosophy, and you find another path that goes from D->B->C->Philosophy, you should can stop sending requests after you hit B. Same for caching failures (either dead end or hitting a loop). I've coded a version without caching an version with caching, and the number of HTTP requests have gone from 903 to 451 for 50 random articles.  Caching causes an huge improvement, because the articles often follow the same path to philosophy.
**without caching:** inefficientFindXPathsFromRandomArticles
**with caching:** findPathToPhilosophyFromRandomArticles

 - I also reduce the number of requests required by asking the wiki api for all X number of random articles in one request.

 - **Further Potential Ultimate Improvement**: Downloading wikipedia and using a local copy of the database would eliminate the need for HTTP requests almost entirely, but we would not have the most up to date information or would need to constantly redownload.


Improvements
------------
Currently the wikipedia API only allows a user to retrieve the links on a page in alphabetical order. One way to improve performance would be to add support to the the Wiki API to allow the retrieval of links by order of appearance in the article. This would cut down on the network traffic as we would not need to retrieve the entirety of the article. And this is probably a feasible request since Wikipedia is open sourced (we could even implement this ourselves and submit a pull request!). Though if we include editing wikipedia's source code as a possibility, we could implement this entire search on their server.

Issues
------
Some articles have an hanging open parenthesis, braces, or reference tags which will cause issues for the parsing, causing no link to be found because everything is considered inside of parenthesis. I've improved this greatly by ignoring braces/parenthesis/ref tags in comments, but this does cause some false negatives. This could be solved with a more sophisticated parser that could detect these issues, but for now, pages with invalid syntax are treated as dead ends.

Classes:
--------

 - WikiArticleRequester - responsible for making requests to the Wiki API to retrieve articles
 - WikiPageParser - responsible for parsing page data to find the first legitimate link
 - WikiCrawler - crawls wikipedia using the above two classes to find paths to the Philosophy article
 - CrawlerResult - represents one result from the crawler
 - CrawlerResults - represents a set of CrawlerResults and can print stats on itself


## Note on Styling ##
I realize I am not strictly following the best PEP guidelines for styling, but this is mainly because I am used to my company's styling (or atleast my team's styling). I'm think the main purpose of a style guide is to keep things consistent and readable, so I would definitely be willing to learn new standards.

