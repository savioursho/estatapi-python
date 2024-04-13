import pytest

from estatapi import _enum

test_data_api_type = (
    ["value", "expected"],
    [
        pytest.param("getStatsList", "getStatsList", id="getStatsList"),
        pytest.param("getMetaInfo", "getMetaInfo", id="getMetaInfo"),
        pytest.param("getStatsData", "getStatsData", id="getStatsData"),
        pytest.param("refDataset", "refDataset", id="refDataset"),
        pytest.param("getDataCatalog", "getDataCatalog", id="getDataCatalog"),
        pytest.param("getStatsDatas", "getStatsDatas", id="getStatsDatas"),
    ],
)


class TestApiType:
    @pytest.mark.parametrize(*test_data_api_type)
    def test_members(self, value, expected):
        api_type = _enum.ApiType[value]
        assert api_type == expected


test_data_response_data_type = (
    ["value", "expected"],
    [
        pytest.param("XML", "xml", id="xml"),
        pytest.param("JSON", "json", id="json"),
        pytest.param("JSONP", "jsonp", id="jsonp"),
        pytest.param("CSV", "csv", id="csv"),
    ],
)


class TestResponseDataType:
    @pytest.mark.parametrize(*test_data_response_data_type)
    def test_members(self, value, expected):
        response_data_type = _enum.ResponseDataType[value]
        assert response_data_type == expected
