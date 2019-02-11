from Extractors.Extractor import Extractor
from collections import Mapping
import re
import sys
import pandas as pd
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

    def _wordCount(self, body):
        exp = re.compile(r'<.*?>') #Answers has html :)
        answer = exp.sub('', body)
        return len(answer.split())

    def getAllAnswerWordCount(self, answers):
        wordCountList = []
        for answerIndex in answers:
            answers[answerIndex]['WordCount'] = self._wordCount(answers[answerIndex]['Body'])
            wordCountList.append(answers[answerIndex]['WordCount'])
        return wordCountList

    def getAllAnswerScoreList(self, answers):
        scoreList = []
        for answerIndex in answers:
            scoreList.append(answers[answerIndex]['Score'])
        return scoreList

    def getAllAnswerUserIdList(self, answers):
        scoreList = []
        for answerIndex in answers:
            scoreList.append(answers[answerIndex]['Score'])
        return scoreList

    def getAllAnswerAcceptanceList(self, questions):
        acceptedAnswers = self.getAcceptedAnswers(questions)
        return self.getAnswerAcceptanceList(acceptedAnswers)

    def getAnswerAcceptanceList(self, acceptedAnswers):
        answers = self.posts['answers']
        answerAcceptanceList = []

        for answerIndex in answers:
            answer = answers[answerIndex]
            answerAcceptance = 0
            if answer['Id'] in acceptedAnswers:
                answerAcceptance = 1
            answerAcceptanceList.append(answerAcceptance)
        return answerAcceptanceList

    def getAcceptedAnswers(self, questions):
        questions = self.posts['questions']
        acceptedAnswers = []

        for questionIndex in questions:
            question = questions[questionIndex]
            if 'AcceptedAnswerId' in question:
                acceptedAnswers.append(question['AcceptedAnswerId'])

        return acceptedAnswers

    def getPdSeries(self):
        print('Getting series...')
        parsed_xml = self.tree
        dfcols = ['WordCount', 'UserId', 'Score', 'Accepted']
        df_xml = pd.DataFrame(columns=dfcols)
        answers = self.getRawAnswers()
        acceptance_list = self.getAcceptedAnswers(self.posts['questions'])


        for node in answers:
            sys.stdout.write('.')
            sys.stdout.flush()
            body = node.attrib.get('Body')

            wordCount = self._wordCount(body)
            if (wordCount is not None):
                wordCount = int(wordCount)

            score = node.attrib.get('Score')
            if (score is not None):
                score = int(score)

            userId = node.attrib.get('OwnerUserId')
            if (userId is not None):
                userId = int(userId)
            else:
                userId = 0

            accepted = (node.attrib.get('Id') in acceptance_list)
            df_xml = df_xml.append(pd.Series([wordCount, score, userId, accepted], index=dfcols), ignore_index=True)

        print('Series ready!')
        return df_xml
