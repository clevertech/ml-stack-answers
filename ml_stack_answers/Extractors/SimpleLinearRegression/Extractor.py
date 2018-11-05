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
        x = [] # list of wordcounts for all posts
        y = [] # corresponding accepted / not accepted status of all posts
        XandY = [x,y]

        return [x,y]
        # for each question
            # get question's set of answers
            # get each answer's author's score ( author_score )
            # get each answer's word count (word_count)
            # get number of upvotes on answer (upvotes)
            # answer_score = author_score*5 + word_count*2 + upvotes
            # answer_accepted = True or False
