#-*- coding:utf-8 -*-
import pytest
import farine.utils
from fixtures import *


def test_suppress_silent():
    with farine.utils.suppress(ValueError):
        raise ValueError


def test_suppress_raises():
    with pytest.raises(ValueError) as e:
        with farine.utils.suppress((RuntimeError, ZeroDivisionError)):
            raise ValueError
    assert e.type == ValueError
