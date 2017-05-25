#-*- coding:utf-8 -*-
import time
import pytest
import farine.utils
import farine.exceptions
from fixtures import *


def test_suppress_silent():
    with farine.utils.suppress(ValueError):
        raise ValueError

def test_suppress_raises():
    with pytest.raises(ValueError) as e:
        with farine.utils.suppress((RuntimeError, ZeroDivisionError)):
            raise ValueError
    assert e.type == ValueError

def test_timeout_ok():
    with farine.utils.Timeout(5):
        time.sleep(0.1)

def test_timeout_none_ok():
    with farine.utils.Timeout(None):
        time.sleep(0.1)

def test_timeout_raise():
    with pytest.raises(farine.exceptions.TimeoutError) as e:
        with farine.utils.Timeout(1):
            time.sleep(2)
    assert e.type == farine.exceptions.TimeoutError
