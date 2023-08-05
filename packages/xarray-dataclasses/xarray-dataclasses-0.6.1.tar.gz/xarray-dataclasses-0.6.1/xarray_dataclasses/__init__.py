# flake8: noqa
# type: ignore
__author__ = "Akio Taniguchi"
__version__ = "0.6.1"


# for Python 3.7 - 3.8
def _make_field_generic():
    from dataclasses import Field
    from typing import Sequence

    GenericAlias = type(Sequence[int])
    Field.__class_getitem__ = classmethod(GenericAlias)


_make_field_generic()


# submodules
from . import dataarray
from . import dataset
from . import deprecated
from . import datamodel
from . import typing
from . import utils


# aliases
from .dataarray import *
from .dataset import *
from .deprecated import *
from .datamodel import *
from .typing import *
