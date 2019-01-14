from helpers import get_data_directory, data_files
from Extractors.PostExtractor import PostExtractor

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def run(ctx, data, predict):
    """Preprocess data files for algorithm"""
    data_dir = ensureDirSlash(data)
    predict = predict.split(',')

    extracted_posts = PostExtractor(data_dir + files['Posts'])
    x = PostExtractor.getWordCountOfAllAnswers(extracted_posts.posts['answers']) # list of wordcounts for all posts
    y = PostExtractor.getAllAnswerAcceptanceList(extracted_posts.posts['questions']) # corresponding accepted / not accepted status of all posts

    # Splitting the dataset into the Training set and Test set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/3, random_state=0)

    # Fitting Multiple Linear Regression to the Training set
    regressor = LinearRegression()
    regressor.fit(x_train, y_train)

    to_predict = [[float(n)] for n in predict]
    predicted = regressor.predict(to_predict)
    return predicted
