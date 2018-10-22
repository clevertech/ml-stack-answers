# -*- coding: utf-8 -*-

"""Console script for ml_stack_answers."""
import sys
import click
import pprint
from os import path

from Extractors.SimpleLinearRegression.Extractor import SimpleLinearRegressionExtractor

files = {
    'Badges': 'Badges.xml',
    'Comments': 'Comments.xml',
    'PostHistory': 'PostHistory.xml',
    'PostLinks': 'PostLinks.xml',
    'Posts': 'Posts.xml',
    'Tags': 'Tags.xml',
    'Users': 'Users.xml',
    'Votes': 'Votes.xml',
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
@click.option("--data", default="./data/", help="Path to folder containing the data files to preprocess.  Looks for the following files: \n" + pprint.pformat(files))
@click.pass_context
def preprocess(ctx, data):
    """Preprocess data files for algorithm"""
    data_dir = ensureDirSlash(data)

    if isMissingFile(data):
        print("Missing files.  run preprocess with --data")
        exit(100)
    else:
        print("Found datafiles")

    SimpleLinearRegressionExtractor(data_dir, files)
    # slr_features = SimpleLinearRegressionExtractor(data_dir, files).getFeatures()
    # slr_model = train_model
    # slr_predictions = guess_unanswered

    click.echo("TODO: Preprocess data")
    return 0

main.add_command(preprocess)


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
