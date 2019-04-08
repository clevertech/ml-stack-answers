# -*- coding: utf-8 -*-

"""Console script for ml_stack_answers."""
import sys
import click
import matplotlib.pyplot as plt
import Algorithms.SLR as SLR
from os import path
import pprint
pp = pprint.PrettyPrinter(indent=4)

import numpy
numpy.set_printoptions(threshold=numpy.nan)

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
@click.pass_context
def slr(ctx):
    print(SLR(ctx, data_dir))
main.add_command(slr)

@click.command()
@click.pass_context
def mlr(ctx):
    pairs = MLR(ctx, data_dir)
    for pair in pairs:
        print(pair)
main.add_command(mlr)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
