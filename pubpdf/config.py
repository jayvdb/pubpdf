# -*- coding: utf-8 -*-
"""Configuration module."""
from __future__ import absolute_import
from __future__ import unicode_literals

import sys

from logging import getLogger
from os.path import expanduser
from textwrap import dedent

import configargparse

__logs__ = getLogger(__package__)
_options = None


def get_parser():
    """Get config parser."""
    parser = configargparse.ArgParser(
        prog=__package__,
        usage='%(prog)s [options] pid [pid]',
        description=dedent(
            """
            pubpdf produces a publications list.
            """.rstrip()),
        default_config_files=['~/.pubpdfrc', '.pubpdfrc', '~/.pubrc', '.pubrc'])

    parser.add('-c', '--config', is_config_file=True,
               help='config file path')

    parser.add('--oai-api', required=True,
               help='OAI API URL')

    parser.add('--oai-format', required=True,
               help='OAI format', default='mods')

    parser.add('--oai-identifier-prefix', help='OAI identifier prefix')

    parser.add('--check-oai-repo',
               help='Iterate over all publications in repository',
               action='store_true')

    parser.add('--csl-style',
               help='CSL style name')

    parser.add('--csl-style-dir',
               help='Directory containing CSL style files')

    parser.add('--group-by-type', help='Group types of publicatons together',
               action='store_true')

    parser.add('--html-preamble', default='<html>\n  <body>\n')

    parser.add('--output-file', help='Output filename', default='pubs.pdf')

    parser.add('pids', nargs='*', help='pids (identifiers)')

    return parser


def get_options():
    """Get options."""
    global _options

    if not _options:
        parser = get_parser()

        pytest = sys.argv[0].endswith('/py.test')
        args = [] if pytest else None

        try:
            _options = parser.parse_args(args=args)
        except SystemExit:
            if pytest:
                __logs__.warning('failed to load options')
                return

            raise

        _options.output_file = expanduser(_options.output_file)
        _options.csl_style_dir = expanduser(_options.csl_style_dir)

    return _options
