"""hydroMT plugin for fiat models."""

from os.path import dirname, join, abspath

# NOTE version number without "v"
__version__ = "0.2.0"

DATADIR = join(dirname(abspath(__file__)), "data")

from .fiat import *
