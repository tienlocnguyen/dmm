import time

import pytest

from dmm.controllers.v86d.controller import V86DController


@pytest.fixture(autouse=True)
def v86d():
    return V86DController("/dev/ttyUSB0")


def test_connect(v86d):
    assert v86d.connect()


def test_disconnect(v86d):
    assert v86d.connect()
    assert v86d.disconnect()


def test_connect_status(v86d):
    assert v86d.connect()
    assert v86d.is_connected()
    assert v86d.disconnect()
    assert not v86d.is_connected()


def test_start_stop(v86d):
    v86d.connect()
    v86d.start()
    time.sleep(10)
    v86d.stop()
