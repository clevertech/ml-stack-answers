# -*- coding: utf-8 -*-

"""Console script for ml_stack_answers."""
import sys
import click


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


@main.command()
@click.option('--data', default='data/', help='Path to folder containing Badges.xml, Comments.xml, PostHistory.xml, PostLinks.xml, Posts.xml, Tags.xml, Users.xml, and Votes.xml (i.e. the extracted archive from StackOverflow)')
@click.pass_context
def preprocess(ctx, data):
    click.echo("TODO: Verify files exist")
    click.echo("TODO: Open a custom Extractor instance for each file, customized with file ")
    click.echo("TODO: Preprocess data")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
