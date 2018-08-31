#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ml_stack_answers` package."""

import pytest

from click.testing import CliRunner

from ml_stack_answers import cli

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

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help' in help_result.output
    assert 'preprocess' in help_result.output

def test_default_data_dir():
    """Test the CLI."""
    print("This test assumes that ./data/ contains all relevant files")
    runner = CliRunner()
    data_result = runner.invoke(cli.main, ['preprocess'])
    for file in files:
        assert file + "is found." in data_result.output
    assert "Missing files." not in data_result.output

def test_invalid_data_dir():
    """Test the CLI."""
    print("This test assumes that ./data/ contains all relevant files")
    runner = CliRunner()
    data_result = runner.invoke(cli.main, ['preprocess', '--data', '/tmp'])
    for file in files:
        assert file + "is not found." in data_result.output
    assert "Missing files" in data_result.output
    assert data_result.exit_code == 100
