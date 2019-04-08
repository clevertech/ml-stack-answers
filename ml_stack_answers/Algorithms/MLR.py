from Extractors.PostExtractor import PostExtractor
import pprint
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

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

pp = pprint.PrettyPrinter(indent=4)


def run(ctx, data_dir):
    """Preprocess data files for algorithm"""

    extracted_posts = PostExtractor(data_dir + files['Posts'])
    pd_posts = extracted_posts.getPdSeries()

    x = pd_posts.iloc[:, :3].values  ## independent
    y = pd_posts.iloc[:, -1:].values ## depdendent

    print('Finished extracing series')

    # Splitting the dataset into the Training set and Test set
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/3, random_state=0)
    print('Finished splitting series')

    # Fitting Simple Linear Regression to the Training set
    regressor = LinearRegression()
    regressor.fit(x_train, y_train)

    print('Finished fitting series')

    predicted = regressor.predict(x_test)

    #visualize results
    plt.scatter(x_test[:1], y_test)
    plt.plot(y_test, predicted)
    plt.show()

    plt.scatter(x_test[1:2], y_test)
    plt.plot(y_test, predicted)
    plt.show()

    plt.scatter(x_test[2:3], y_test)
    plt.plot(y_test, predicted)
    plt.show()


    return zip(y_test, predicted)

