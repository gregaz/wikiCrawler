
class WikiPageParser():
    """The main purpose of this class is to parse the raw page, and find the first valid link.
    Could use a parsing library, but it would be slower for this application as we do not need
    to parse the entire page."""

    rawPageString = ''

    def __init__(self, rawPageString=''):
        self.rawPageString = rawPageString

    def getFirstLegitimateLinkTitleForString(self,rawPageString):
        self.rawPageString = rawPageString
        return self.getFirstLegitimateLinkTitle()

    def isStringValidLink(self,aString):
        if 'File:' in aString:
            return False
        elif 'image:' in aString:
            return False
        elif 'wikt:' in aString:
            return False
        elif 'wiktionary:' in aString:
            return False
        elif len(aString.split('|')) > 2:
            return False
        else:
            return True

    def getFirstLegitimateLinkTitle(self):
        """The first legitimate link is the first link that is not italicized or inside parenthesis.
        Be sure that we only start looking in the main body article by ignoring links inside braces"""
        braceCount = 0
        bracketCount = 0
        parenthesisCount = 0
        footnoteCount = 0
        carrotCount = 0
        lastCarrotCount = 0
        inComment = False
        linkTitle = ''
        for i,char in enumerate(self.rawPageString):
            #ignore anything in a comment block
            if inComment:
                if char == '-':
                    try:
                        if self.rawPageString[i:i+3] == '-->':
                            inComment = False
                    except:
                        print('End of file error')
                        return None
                else:
                    continue

            if char == '{':
                braceCount += 1
            elif char == '}':
                braceCount -= 1
            elif char == '(' and bracketCount == 0 and braceCount == 0:
                parenthesisCount += 1
            elif char == ')' and bracketCount == 0 and braceCount == 0:
                parenthesisCount -= 1
            elif char == '<':
                carrotCount += 1
                #try incase we hit the end of the file
                try:
                    if self.rawPageString[i:i+4] == '<ref':
                        footnoteCount += 1
                        lastCarrotCount = carrotCount
                    elif self.rawPageString[i:i+6] == '</ref>':
                        footnoteCount -= 1
                    elif self.rawPageString[i:i+4] == '<!--':
                        inComment = True
                except:
                    print('End of file Error')
                    return None
            elif char == '/':
                if carrotCount == lastCarrotCount and footnoteCount > 0:
                    try:
                        if self.rawPageString[i:i+2] == '/>':
                            footnoteCount -= 1
                    except:
                        print('End of file Error')
                        return None
            elif char == '>':
                carrotCount -= 1
            elif braceCount == 0 and parenthesisCount == 0 and footnoteCount == 0 and carrotCount == 0:
                if char == '[':
                    bracketCount = bracketCount + 1
                elif char == ']':
                    if bracketCount != 2:
                        bracketCount -=  1
                    elif not self.isStringValidLink(linkTitle):
                        bracketCount -= 1
                        linkTitle = ''
                    else:
                        #links are formatted as [article title for link | link label]
                        #specific subheadings within the article do not work with the api, just use the main article here
                        linkWithoutLabel = linkTitle.split('|')[0]
                        linkWithoutSubHeading = linkWithoutLabel.split('#')[0]
                        return linkWithoutSubHeading
                elif bracketCount == 2:
                    linkTitle = linkTitle + char
        #print([braceCount, bracketCount, parenthesisCount, footnoteCount, carrotCount])
        return None