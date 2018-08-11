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
@click.pass_context
def preprocess(ctx):
    click.echo("TODO: Preprocess data")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
