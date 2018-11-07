from Extractors.SimpleLinearRegression.Posts.PostExtractor import PostExtractor
import pprint

pp = pprint.PrettyPrinter(indent=4)


class SimpleLinearRegressionExtractor:
    def __init__(self, data_dir, files):
        print("Prepping Post SLR Extractor")
        self.extracted_posts = PostExtractor(data_dir + files['Posts'])
        # todo: initiate SLR extractor for Comments
        # todo: initiate SLR extractor for PostHistory
        # todo: initiate SLR extractor for PostLinks
        # todo: initiate SLR extractor for Tags
        # todo: initiate SLR extractor for Badges
        # todo: initiate SLR extractor for Users
        # todo: initiate SLR extractor for Votes

        # self.getFeatures(data_map)

    """
    Returns a map, keyed by Post IDs,  features to their values, key
    """
    def getXandY(self):
        print("Getting independent variable (x)")
        x = self.getWordCountOfAllAnswers() # list of wordcounts for all posts
        print("Getting dependent variable (y)")
        y = self.getAllAnswerAcceptanceList() # corresponding accepted / not accepted status of all posts
        print("y is:")
        pp.pprint(y)
        return [x,y]
        # both of these lists should be of length N where N is the size equal to the length of extracted_posts[answers]
        #  [200,300,150] # wordcount of answers
        #  [100,0,100] # accepted status of answers

    def getWordCountOfAllAnswers(self):
        return []

    def getAllAnswerAcceptanceList(self):
        acceptedAnswers = self.getAcceptedAnswers()
        return self.getAnswerAcceptanceList(acceptedAnswers)

    def getAnswerAcceptanceList(self, acceptedAnswers):
        answers = self.extracted_posts.posts['answers']
        answerAcceptanceList = []

        for answerIndex in answers:
            answer = answers[answerIndex]
            answerAcceptance = 0
            if answer['Id'] in acceptedAnswers:
                answerAcceptance = 1
            print('Answer '+str(answer['Id'])+' is '+str(answerAcceptance)+"\n")
            answerAcceptanceList.append(answerAcceptance)
        return answerAcceptanceList

    def getAcceptedAnswers(self):
        questions = self.extracted_posts.posts['questions']
        acceptedAnswers = []

        for questionIndex in questions:
            question = questions[questionIndex]
            if 'AcceptedAnswerId' in question:
                acceptedAnswers.append(question['AcceptedAnswerId'])

        return acceptedAnswers
