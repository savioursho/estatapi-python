import pytest
from pydantic import ValidationError

from estatapi import _appid, _functions


@pytest.fixture
def register_uri(requests_mock):
    requests_mock.register_uri(
        "GET",
        "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList",
        json={"GET_STATS_LIST": None},
    )
    requests_mock.register_uri(
        "GET",
        "https://api.e-stat.go.jp/rest/3.0/app/json/getMetaInfo",
        json={"GET_META_INFO": None},
    )
    requests_mock.register_uri(
        "GET",
        "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData",
        json={"GET_STATS_DATA": None},
    )


@pytest.fixture
def set_appid():
    # set appid
    _appid.set_appid("sampleappid")
    yield
    # reset appid
    _appid.set_appid()


class TestGetStatsList:
    params_to_be_accepted = [
        {"lang": "J"},
        {"lang": "E"},
        {"surveyYears": None},
        {"surveyYears": "2024"},
        {"surveyYears": "202404"},
        {"surveyYears": "202304-202404"},
        {"openYears": None},
        {"openYears": "2024"},
        {"openYears": "202404"},
        {"openYears": "202304-202404"},
        {"statsField": "01"},
        {"statsField": "9999"},
        {"statsCode": "00000"},
        {"statsCode": "00000"},
        {"statsCode": "00700014"},
        {"searchWord": "tokyo"},
        {"searchWord": "tokyo AND population"},
        {"searchKind": "1"},
        {"searchKind": "2"},
        {"collectArea": "1"},
        {"collectArea": "2"},
        {"collectArea": "3"},
        {"explanationGetFlg": "Y"},
        {"explanationGetFlg": "N"},
        {"statsNameList": "Y"},
        {"statsNameList": None},
        {"startPosition": 1},
        {"startPosition": None},
        {"limit": None},
        {"limit": 1},
        {"updatedDate": None},
        {"updatedDate": "2024"},
        {"updatedDate": "202412"},
        {"updatedDate": "20241231"},
        {"updatedDate": "19951231-20241231"},
    ]

    params_to_be_rejected = [
        {"lang": "invalid_value"},
        {"surveyYears": "invalid_value"},
        {"surveyYears": "2024-04"},
        {"surveyYears": "2024-202404"},
        {"surveyYears": "20230401"},
        {"openYears": "invalid_value"},
        {"openYears": "2024-04"},
        {"openYears": "20230401"},
        {"statsField": "0"},
        {"statsField": "111"},
        {"statsField": "aaaa"},
        {"statsCode": "1111"},
        {"statsCode": "aaaaa"},
        {"searchWord": ["list", "is", "invalid"]},
        {"searchKind": "3"},
        {"searchKind": "01"},
        {"collectArea": "4"},
        {"collectArea": "a"},
        {"explanationGetFlg": "Yes"},
        {"explanationGetFlg": 1},
        {"statsNameList": "N"},
        {"statsNameList": 1},
        {"startPosition": 0},
        {"startPosition": -1},
        {"startPosition": "a"},
        {"limit": -1},
        {"limit": "a"},
        {"updatedDate": "24"},
        {"updatedDate": "aaaa"},
        {"updatedDate": "202401-202412"},
        {"updatedDate": "20249999"},
    ]

    def test_root_key(self, register_uri, set_appid):
        """Root key must be 'GET_STATS_LIST'"""
        output = _functions.get_stats_list()
        output = output.to_json()
        assert list(output.keys()) == ["GET_STATS_LIST"]

    @pytest.mark.parametrize(
        "params", params_to_be_accepted, ids=[str(p) for p in params_to_be_accepted]
    )
    def test_validate_accepted(self, params, register_uri, set_appid):
        """This parameters should be accepted."""
        try:
            _functions.get_stats_list(**params)
        except ValidationError:
            pytest.fail("This parameter should be accepted, but is rejected.")

    @pytest.mark.parametrize(
        "params", params_to_be_rejected, ids=[str(p) for p in params_to_be_rejected]
    )
    def test_validate_rejected(self, params, register_uri, set_appid):
        """This parameters should be rejected."""
        try:
            _functions.get_stats_list(**params)
        except ValidationError:
            assert True
        else:
            pytest.fail("This parameter should be rejected, but is accepted.")


class TestGetMetaInfo:
    params_to_be_accepted = [
        {"statsDataId": "0000000000", "lang": "J"},
        {"statsDataId": "0000000000", "lang": "E"},
        {"statsDataId": "0000000000"},
        {"statsDataId": "0000000000", "explanationGetFlg": "Y"},
        {"statsDataId": "0000000000", "explanationGetFlg": "N"},
    ]

    params_to_be_rejected = [
        {"statsDataId": "0000000000", "lang": "invalid_value"},
        {"statsDataId": "0000000000", "explanationGetFlg": "invalid"},
        {"statsDataId": 1},
        {},
    ]

    def test_root_key(self, register_uri, set_appid):
        """Root key must be 'GET_META_INFO'"""

        params = {"statsDataId": "0000000000"}
        output = _functions.get_meta_info(**params)
        output = output.to_json()
        assert list(output.keys()) == ["GET_META_INFO"]

    @pytest.mark.parametrize(
        "params", params_to_be_accepted, ids=[str(p) for p in params_to_be_accepted]
    )
    def test_validate_accepted(self, params, register_uri, set_appid):
        """This parameters should be accepted."""
        try:
            _functions.get_meta_info(**params)
        except ValidationError:
            pytest.fail("This parameter should be accepted, but is rejected.")

    @pytest.mark.parametrize(
        "params", params_to_be_rejected, ids=[str(p) for p in params_to_be_rejected]
    )
    def test_validate_rejected(self, params, register_uri, set_appid):
        """This parameters should be rejected."""
        try:
            _functions.get_meta_info(**params)
        except ValidationError:
            assert True
        else:
            pytest.fail("This parameter should be rejected, but is accepted.")


class TestGetStatsData:
    params_to_be_accepted = [
        {"dataSetId": "0000000000"},
        {"statsDataId": "0000000000"},
        {"dataSetId": "0000000000", "lvTab": "aaaa"},
        {"dataSetId": "0000000000", "cdTab": "aaaa"},
        {"dataSetId": "0000000000", "cdTabFrom": "aaaa"},
        {"dataSetId": "0000000000", "cdTabTo": "aaaa"},
        {"dataSetId": "0000000000", "lvTime": "aaaa"},
        {"dataSetId": "0000000000", "cdTime": "aaaa"},
        {"dataSetId": "0000000000", "cdTimeFrom": "aaaa"},
        {"dataSetId": "0000000000", "cdTimeTo": "aaaa"},
        {"dataSetId": "0000000000", "lvArea": "aaaa"},
        {"dataSetId": "0000000000", "cdArea": "aaaa"},
        {"dataSetId": "0000000000", "cdAreaFrom": "aaaa"},
        {"dataSetId": "0000000000", "cdAreaTo": "aaaa"},
        {"dataSetId": "0000000000", "lvCat01": "aaaa"},
        {"dataSetId": "0000000000", "cdCat01": "aaaa"},
        {"dataSetId": "0000000000", "cdCat01From": "aaaa"},
        {"dataSetId": "0000000000", "cdCat01To": "aaaa"},
        {"dataSetId": "0000000000", "lvCat15": "aaaa"},
        {"dataSetId": "0000000000", "cdCat15": "aaaa"},
        {"dataSetId": "0000000000", "cdCat15From": "aaaa"},
        {"dataSetId": "0000000000", "cdCat15To": "aaaa"},
        {"dataSetId": "0000000000", "startPosition": 1},
        {"dataSetId": "0000000000", "limit": None},
        {"dataSetId": "0000000000", "limit": 1},
        {"dataSetId": "0000000000", "metaGetFlg": "Y"},
        {"dataSetId": "0000000000", "metaGetFlg": "N"},
        {"dataSetId": "0000000000", "cntGetFlg": "Y"},
        {"dataSetId": "0000000000", "cntGetFlg": "N"},
        {"dataSetId": "0000000000", "explanationGetFlg": "Y"},
        {"dataSetId": "0000000000", "explanationGetFlg": "N"},
        {"dataSetId": "0000000000", "annotationGetFlg": "Y"},
        {"dataSetId": "0000000000", "annotationGetFlg": "N"},
        {"dataSetId": "0000000000", "replaceSpChar": 0},
        {"dataSetId": "0000000000", "replaceSpChar": 3},
        ####
        {"statsDataId": "0000000000", "lang": "J"},
        {"statsDataId": "0000000000", "lang": "E"},
        {"statsDataId": "0000000000", "explanationGetFlg": "Y"},
        {"statsDataId": "0000000000", "explanationGetFlg": "N"},
    ]

    params_to_be_rejected = [
        {"dataSetId": 1},
        {"statsDataId": 1},
        {"statsDataId": "0000000000", "dataSetId": "0000000000"},
        {"dataSetId": "0000000000", "lvCat15": 1},
        {"dataSetId": "0000000000", "lvCat16": "aaaa"},
        {"dataSetId": "0000000000", "cdCat16": "aaaa"},
        {"dataSetId": "0000000000", "cdCat16From": "aaaa"},
        {"dataSetId": "0000000000", "cdCat16To": "aaaa"},
        {"dataSetId": "0000000000", "invalid_arg": "aaaa"},
        {"dataSetId": "0000000000", "startPosition": 0},
        {"dataSetId": "0000000000", "limit": 0},
        {"dataSetId": "0000000000", "metaGetFlg": 1},
        {"dataSetId": "0000000000", "cntGetFlg": 1},
        {"dataSetId": "0000000000", "explanationGetFlg": 1},
        {"dataSetId": "0000000000", "annotationGetFlg": 1},
        {"dataSetId": "0000000000", "replaceSpChar": 4},
        {"dataSetId": "0000000000", "replaceSpChar": "a"},
        {"statsDataId": "0000000000", "lang": "invalid_value"},
        {},
    ]

    def test_root_key(self, register_uri, set_appid):
        """Root key must be 'GET_STATS_DATA'"""

        params = {"statsDataId": "0000000000"}
        output = _functions.get_stats_data(**params)
        output = output.to_json()
        assert list(output.keys()) == ["GET_STATS_DATA"]

    @pytest.mark.parametrize(
        "params", params_to_be_accepted, ids=[str(p) for p in params_to_be_accepted]
    )
    def test_validate_accepted(self, params, register_uri, set_appid):
        """This parameters should be accepted."""
        try:
            _functions.get_stats_data(**params)
        except ValidationError:
            pytest.fail("This parameter should be accepted, but is rejected.")

    @pytest.mark.parametrize(
        "params", params_to_be_rejected, ids=[str(p) for p in params_to_be_rejected]
    )
    def test_validate_rejected(self, params, register_uri, set_appid):
        """This parameters should be rejected."""
        try:
            _functions.get_stats_data(**params)
        except ValidationError:
            assert True
        except ValueError as e:
            assert (
                "Only one of dataSetId and statsDataId must be specified" in str(e)
            ) or ("Names of arguments are invalid" in str(e))
        else:
            pytest.fail("This parameter should be rejected, but is accepted.")
