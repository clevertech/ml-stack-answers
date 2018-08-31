# -*- coding: utf-8 -*-

"""Console script for ml_stack_answers."""
import sys
import click
import pprint
from os import path

files = [
    'Badges.xml',
    'Comments.xml',
    'PostHistory.xml',
    'PostLinks.xml',
    'Posts.xml',
    'Tags.xml',
    'Users.xml',
    'Votes.xml',
]

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def main(ctx, debug):
    """Console script for ml_stack_answers."""
    ctx.obj = dict()
    ctx.obj['DEBUG'] = debug
    click.echo("Replace this message by putting your code into "
               "ml_stack_answers.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


@click.command()
@click.option("--data", default="data/", help="Path to folder containing the data files to preprocess.  Looks for the following files: \n" + pprint.pformat(files))
@click.pass_context
def preprocess(ctx, data):
    """Preprocess data files for algorithm"""
    data = ensureDirSlash(data)

    if isMissingFile():
        print("Missing files")
        exit(100)

    # invoke SLR extractor

    click.echo("TODO: Open a custom Extractor instance for each file, customized with file ")
    click.echo("TODO: Preprocess data")
    return 0

main.add_command(preprocess)


def isMissingFile():
    missingFile = False
    for file in files:
        fileFound = path.isFile(data + file)
        print(file + " is " + ("found" if fileFound else "not found."))
        missingFile = missingFile or not fileFound
    return missingFile


def ensureDirSlash(dir):
    if (dir[-1] is not '/'):
        dir = dir + '/'

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
