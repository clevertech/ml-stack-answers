# -*- coding: utf-8 -*-

"""Console script for ml_stack_answers."""
import sys
import click
import pprint
import matplotlib.pyplot as plt
from os import path
from pprint import pprint as pp

from Extractors.SimpleLinearRegression.Extractor import SimpleLinearRegressionExtractor

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

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def main(ctx, debug):
    """Console script for ml_stack_answers."""
    ctx.obj = dict()
    ctx.obj['DEBUG'] = debug
    return 0


@click.command()
@click.option("--data", default="./data/", help="Path to folder containing the data files to slr.  Looks for the following files: \n" + pprint.pformat(files))
@click.argument("predict")
@click.pass_context
def slr(ctx, data, predict):
    """Preprocess data files for algorithm"""
    data_dir = ensureDirSlash(data)
    predict = predict.split(',')

    if isMissingFile(data):
        print("Missing files.  run slr with --data")
        exit(100)
    else:
        print("Found datafiles")

    slr = SimpleLinearRegressionExtractor(data_dir, files)
    XandY = slr.getXandY()
    # Importing the libraries
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd

    # Importing the dataset
    import csv

    zipXandY = [*zip(*XandY)]

    with open("output.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(zipXandY)

    dataset = pd.read_csv('output.csv')
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1].values

    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=0)

    # Feature Scaling
    """from sklearn.preprocessing import StandardScaler
    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)
    X_test = sc_X.transform(X_test)
    sc_y = StandardScaler()
    y_train = sc_y.fit_transform(y_train)"""

    # Fitting Simple Linear Regression to the Training set
    from sklearn.linear_model import LinearRegression
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    to_predict = [[float(n)] for n in predict]
    pp(to_predict)
    predicted = regressor.predict(to_predict)
    pp(predicted)
    return predicted

main.add_command(slr)


def isMissingFile(data):
    if type(data) is not str:
        return True
    missingFile = False
    for file,filename in files.items():
        fileFound = path.isfile(data + filename)
        print(file + " is " + ("found" if fileFound else "not found."))
        missingFile = missingFile or not fileFound
    return missingFile


def ensureDirSlash(dir):
    if (dir[-1] is not '/'):
        dir = dir + '/'
    return dir

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
