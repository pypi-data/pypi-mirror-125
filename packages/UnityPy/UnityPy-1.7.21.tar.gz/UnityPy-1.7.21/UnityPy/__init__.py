__version__ = "1.7.21"

from .environment import Environment


def load(*args):
    return Environment(*args)


# backward compatibility
AssetsManager = Environment
