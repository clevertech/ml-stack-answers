from Extractors.Extractor import Extractor
from collections import Mapping
import pprint

pp = pprint.PrettyPrinter(indent=4)

class PostExtractor(Extractor):
    def __init__(self, file):
        print("Prepping PostExtractor")
        super().__init__(file)
        self.posts = {}
        print(self.root)

        # extract
        print("Extracting Q&A from Posts")
        self.posts = self.extractQuestionsAndAnswers()

        print("Extracted")
        return

    def extractQuestionsAndAnswers(self):
        qa = {}
        qa['questions'] = self.getQuestions()
        qa['answers'] = self.getAnswers()
        qa['answersByQuestion'] = self.mapAnswersToQuestions(qa)
        return qa

    def mapAnswersToQuestions(self,qa):
        map = {} # { 'questionId': ['answerId', ...] }
        for answerIndex in qa['answers']:
            answer = qa['answers'][answerIndex]
            if not answer['ParentId'] in map:
                map[answer['ParentId']] = [answer['Id']]
            else:
                map[answer['ParentId']].append(answer['Id'])
        return map

    def getQuestions(self):
        rawQuestions = self.getRawQuestions()
        return self.makeDictFromRawPosts(rawQuestions)

    def getAnswers(self):
        rawAnswers = self.getRawAnswers()
        return self.makeDictFromRawPosts(rawAnswers)

    def getRawQuestions(self):
        return self.root.findall(".//*[@PostTypeId='1']")

    def getRawAnswers(self):
        return self.root.findall(".//*[@PostTypeId='2']")

    def makeDictFromRawPosts(self, rawPosts):
        postsDict = {} # {"id": { the other attributes }}
        for post in rawPosts:
            postsDict[post.attrib["Id"]] = post.attrib
        return postsDict


