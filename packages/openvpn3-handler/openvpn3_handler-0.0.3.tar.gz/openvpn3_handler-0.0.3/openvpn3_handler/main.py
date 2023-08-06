from . import io
from sys import argv


def run():
    io.Menu(*argv[1:])
