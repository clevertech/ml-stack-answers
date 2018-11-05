from Extractors.SimpleLinearRegression.Posts.PostExtractor import PostExtractor


class SimpleLinearRegressionExtractor:
    def __init__(self, data_dir, files):
        print("Prepping Post SLR Extractor")
        extracted_posts = PostExtractor(data_dir + files['Posts'])
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
    def getXandY(self, data_map):
        x = self.getWordCountOfAllAnswers() # list of wordcounts for all posts
        y = self.getAllAnswerAcceptanceList() # corresponding accepted / not accepted status of all posts
        return [x,y]
        # both of these lists should be of length N where N is the size equal to the length of extracted_posts[answers]
        #  [200,300,150] # wordcount of answers
        #  [100,0,100] # accepted status of answers

    def getWordCountOfAllAnswers(self):
        return []

    def getAllAnswerAcceptanceList(self):
        return []
