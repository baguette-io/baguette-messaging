#-*- coding:utf-8 -*-
import pytest
import croissant.utils
from fixtures import *


def test_suppress_silent():
    with croissant.utils.suppress(ValueError):
        raise ValueError


def test_suppress_raises():
    with pytest.raises(ValueError) as e:
        with croissant.utils.suppress((RuntimeError, ZeroDivisionError)):
            raise ValueError
    assert e.type == ValueError
