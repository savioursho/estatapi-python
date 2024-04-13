import pytest

from estatapi import _appid

test_data = (
    ["appid", "expected"],
    [pytest.param("aiueo", "aiueo", id="appid1")],
)


@pytest.fixture
def reset_appid():
    _appid.set_appid()
    yield
    _appid.set_appid()


def test_default_appid():
    assert _appid._APPID is None


@pytest.mark.parametrize(*test_data)
def test_set_appid(appid, expected, reset_appid):
    _appid.set_appid(appid)
    assert _appid._APPID == expected


@pytest.mark.parametrize(*test_data)
def test_get_appid(appid, expected, reset_appid):
    _appid._APPID = appid
    appid = _appid.get_appid()
    assert appid == expected


def test_check_appid_raise(reset_appid):
    try:
        _appid._check_appid()
    except ValueError as e:
        assert "not set" in str(e)
    else:
        pytest.fail("This function should raise exception, but it didn't.")


def test_check_appid_success(reset_appid):
    _appid.set_appid("aiueo")
    _appid._check_appid()
