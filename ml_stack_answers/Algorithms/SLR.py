from Extractors.PostExtractor import PostExtractor
import pprint
pp = pprint.PrettyPrinter(indent=4)

files = {
#    'Badges': 'Badges.xml',
#    'Comments': 'Comments.xml',
#    'PostHistory': 'PostHistory.xml',
#    'PostLinks': 'PostLinks.xml',
    'Posts': 'Posts.xml',
#    'Tags': 'Tags.xml',
#    'Users': 'Users.xml',
#    'Votes': 'Votes.xml',
}

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def run(ctx, data_dir):
    """Preprocess data files for algorithm"""

    extracted_posts = PostExtractor(data_dir + files['Posts'])
    pd_posts = extracted_posts.getPdSeries()

    x = pd_posts.iloc[:, :1].values  ## independent
    y = pd_posts.iloc[:, -1:].values ## depdendent

    print('Finished extracing series')
    pp.pprint(y)

    # Splitting the dataset into the Training set and Test set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/3, random_state=0)
    print('Finished splitting series')

    x_train = np.array(x_train)
    x_train = x_train.astype(np.float64)
    x_train = np.reshape(x_train, (-1,1))

    # Fitting Simple Linear Regression to the Training set
    regressor = LinearRegression()
    regressor.fit(x_train, y_train)

    predicted = regressor.predict(y_test)

    #visualize results
    plt.scatter(x_test, y_test)
    plt.plot(x_test, predicted)
    plt.show()

    return predicted
