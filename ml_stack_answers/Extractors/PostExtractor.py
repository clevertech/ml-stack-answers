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
            df_xml = df_xml.append(self.get_node_pd_series(node, is_question=0), ignore_index=True)

        print('Series ready!')
        return df_xml

    def getQuestionsPdSeries(self):
        print('Getting series...')
        parsed_xml = self.tree
        dfcols = ['WordCount', 'UserId', 'Score', 'Accepted']
        df_xml = pd.DataFrame(columns=dfcols)
        answers = self.getRawAnswers()
        acceptance_list = self.getAcceptedAnswers(self.posts['questions'])

        for node in answers:
            sys.stdout.write('.')
            sys.stdout.flush()
            df_xml = df_xml.append(self.get_node_pd_series(node, is_question=0), ignore_index=True)

        print('Series ready!')
        return df_xml

    def getAnswersPdSeries(self):
        print('Getting series...')
        dfcols = ['WordCount', 'Score', 'UserId', 'Verbs', 'NounPhrases', 'EntityChunks', 'CodeblockCount', 'CommentCount', 'Accepted']
        df_xml = pd.DataFrame(columns=dfcols)
        answers = self.getRawAnswers()

        for node in answers:
            sys.stdout.write('.')
            sys.stdout.flush()
            df_xml = df_xml.append(self.get_node_pd_series(node, is_question=0), ignore_index=True)

        print('Series ready!')
        return df_xml

    def get_node_pd_series(self, node, is_question):
        body = node.attrib.get('Body')
        question_id = node.attrib.get('ParentId')
        question = self.posts['questions'][question_id]

        wordCount = self._wordCount(body)
        if (wordCount is not None):
            word_count = int(wordCount)

        score = node.attrib.get('Score')
        if (score is not None):
            score = int(score)

        userId = node.attrib.get('OwnerUserId')
        if (userId is not None):
            user_id = int(userId)
        else:
            user_id = 0

        # building array for bag_of_verbs
        verbs = node.attrib.get('Verbs').split(',')

        # building array for bag_of_noun_phrases
        noun_phrases = node.attrib.get('NounPhrases').split(',')

        # building array for bag_of_entity_chunks
        entity_chunks = node.attrib.get('EntityChunks').split(',')

        # TODO: build feature for codeblock count
        codeblock_count = node.attrib.get('CodeblockCount')

        # TODO: build feature for comment count
        comment_count = node.attrib.get('CommentCount')

        is_accepted = 1 if (node.attrib.get('Id') == question['AcceptedAnswerId') else 0
        #TODO: Generalize this so we can build a corpus just of text bodies for TF-IDF -- right now, "is_accepted" makes this answer specific
        return pd.Series([word_count, score, user_id, verbs, noun_phrases, entity_chunks, codeblock_count, comment_count, is_accepted], index=dfcols)
