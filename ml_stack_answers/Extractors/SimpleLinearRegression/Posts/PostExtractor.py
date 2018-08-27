from Extractors import Extractor
from collections import Mapping

class PostExtractor(Extractor):
    def __init__(self, path):
        super().__init__(path)
        self.posts = {}

        # extract
        self.posts = self.extractQuestionsAndAnswers(self.root)

        return

    def extractQuestionsAndAnswers(self, root):
        questions = self.getQuestions(root)
        answers = self.getAnswers(root)
        qa_map = self.mapQuestionsToAnswers(questions, answers)

    def mapQuestionsAnswers(self, questions, answers):
        qa_map = {}

        # map answers to questions
        for answer in answers:
            answer_parent = answer['ParentId']
            for question in questions:
                question_id = question['Id']
                if question_id == answer_parent:
                    qa_map = self.pushAnswerIntoQuestionMap(answer, question, qa_map)

    def pushAnswerIntoQuestionMap(self, answer, question, qa_map):
        if not isinstance(qa_map, Mapping):
            return qa_map

        question_dict = qa_map[question['Id']]
        if not isinstance(question_dict, Mapping):
            qa_map[question['Id']] = {}
            question_dict = qa_map[question['Id']]

        answer_dict = question_dict['answers']
        if not isinstance(answer_dict, Mapping):
            question_dict['answers'] = {}
            answer_dict = question_dict['answers']

        answer_dict[answer['Id']] = answer
        return qa_map

    def getQuestions(self,root):
        return root.findall("./[@PostTypeId='1']")

    def getAnswers(self, root):
        return root.findall("./[@PostTypeId='2']")

