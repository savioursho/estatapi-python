import pytest

from estatapi import _appid


@pytest.fixture
def reset_appid():
    _appid.set_appid()
    yield
    _appid.set_appid()


def test_default_appid():
    assert _appid._APPID is None


@pytest.mark.parametrize(
    [
        "arg",
        "expected",
    ],
    [
        pytest.param(
            "aiueo",
            "aiueo",
        )
    ],
)
def test_set_appid(arg, expected, reset_appid):
    _appid.set_appid(arg)
    assert _appid._APPID == expected


@pytest.mark.parametrize(
    [
        "arg",
        "expected",
    ],
    [
        pytest.param(
            "aiueo",
            "aiueo",
        )
    ],
)
def test_get_appid(arg, expected, reset_appid):
    _appid._APPID = arg
    appid = _appid.get_appid()
    assert appid == expected
