# -*- coding: utf-8 -*-

"""Console script for ml_stack_answers."""
import sys
import click
import pprint
import matplotlib.pyplot as plt
import Algorithms.SLR as SLR
from os import path
from pprint import pprint as pp

from Algorithms.SLR import run as SLR
from Algorithms.MLR import run as MLR

data_dir = './data/'

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def main(ctx, debug):
    """Console script for ml_stack_answers."""
    ctx.obj = dict()
    ctx.obj['DEBUG'] = debug
    return 0


@click.command()
@click.argument("predict")
@click.pass_context
def slr(ctx, predict):
    print(SLR(ctx, data_dir, predict))
main.add_command(slr)

@click.command()
@click.argument("predict")
@click.pass_context
def mlr(ctx, predict):
    print(MLR(ctx, data_dir, predict))
main.add_command(mlr)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
