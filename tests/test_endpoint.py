import pytest

from estatapi import _endpoint, _enum

test_data_validate_types_normal = (
    ["api_type", "response_data_type", "expected"],
    [
        pytest.param(
            "getStatsList",
            "XML",
            (_enum.ApiType.getStatsList, _enum.ResponseDataType.XML),
            id="getStatsList-XML",
        ),
        pytest.param(
            "getMetaInfo",
            "JSON",
            (_enum.ApiType.getMetaInfo, _enum.ResponseDataType.JSON),
            id="getMetaInfo-JSON",
        ),
        pytest.param(
            "getStatsData",
            "JSONP",
            (_enum.ApiType.getStatsData, _enum.ResponseDataType.JSONP),
            id="getStatsData-JSONP",
        ),
        pytest.param(
            "refDataset",
            "xml",
            (_enum.ApiType.refDataset, _enum.ResponseDataType.XML),
            id="refDataset-xml",
        ),
        pytest.param(
            "getDataCatalog",
            "json",
            (_enum.ApiType.getDataCatalog, _enum.ResponseDataType.JSON),
            id="getDataCalalog-json",
        ),
        pytest.param(
            "getStatsDatas",
            "csv",
            (_enum.ApiType.getStatsDatas, _enum.ResponseDataType.CSV),
            id="getStatsDatas-csv",
        ),
    ],
)


@pytest.mark.parametrize(*test_data_validate_types_normal)
def test_validate_types_normal(api_type, response_data_type, expected):
    output = _endpoint._validate_types(api_type, response_data_type)
    assert output == expected


test_data_validate_types_raise_value_error = (
    ["api_type", "response_data_type"],
    [
        pytest.param("refDataset", "CSV", id="refDataset-CSV"),
        pytest.param("getDataCatalog", "CSV", id="getDataCalalog-CSV"),
        pytest.param("getStatsDatas", "JSONP", id="getStatsDatas-JSONP"),
    ],
)


@pytest.mark.parametrize(*test_data_validate_types_raise_value_error)
def test_validate_types_raise_value_error(api_type, response_data_type):
    with pytest.raises(ValueError) as e:
        _endpoint._validate_types(api_type, response_data_type)

    assert "is not allowed" in str(e.value)


test_data_validate_types_raise_key_error = (
    ["api_type", "response_data_type"],
    [
        pytest.param("不正なタイプ", "XML", id="invalid-XML"),
        pytest.param("getStatsList", "不正なタイプ", id="getStatsList-invalid"),
    ],
)


@pytest.mark.parametrize(*test_data_validate_types_raise_key_error)
def test_validate_types_raise_value_error(api_type, response_data_type):
    with pytest.raises(KeyError) as e:
        _endpoint._validate_types(api_type, response_data_type)

    assert str(e.value) == "'不正なタイプ'"


test_data_build_path = (
    ["api_type", "response_data_type", "expected"],
    [
        pytest.param(
            "getStatsList",
            "XML",
            "rest/3.0/app/getStatsList",
            id="getStatsList-XML",
        ),
        pytest.param(
            "getMetaInfo",
            "JSON",
            "rest/3.0/app/json/getMetaInfo",
            id="getMetaInfo-JSON",
        ),
        pytest.param(
            "getStatsData",
            "JSONP",
            "rest/3.0/app/jsonp/getStatsData",
            id="getStatsData-JSONP",
        ),
        pytest.param(
            "refDataset",
            "xml",
            "rest/3.0/app/refDataset",
            id="refDataset-xml",
        ),
        pytest.param(
            "getDataCatalog",
            "json",
            "rest/3.0/app/json/getDataCatalog",
            id="getDataCalalog-json",
        ),
        pytest.param(
            "getStatsDatas",
            "csv",
            "rest/3.0/app/getSimpleStatsDatas",
            id="getStatsDatas-csv",
        ),
    ],
)


@pytest.mark.parametrize(*test_data_build_path)
def test_build_path(api_type, response_data_type, expected):
    path = _endpoint._build_path(api_type, response_data_type)
    assert path == expected


test_data_build = (
    ["api_type", "response_data_type", "expected"],
    [
        pytest.param(
            "getStatsList",
            "XML",
            "https://api.e-stat.go.jp/rest/3.0/app/getStatsList",
            id="getStatsList-XML",
        ),
        pytest.param(
            "getMetaInfo",
            "JSON",
            "https://api.e-stat.go.jp/rest/3.0/app/json/getMetaInfo",
            id="getMetaInfo-JSON",
        ),
        pytest.param(
            "getStatsData",
            "JSONP",
            "https://api.e-stat.go.jp/rest/3.0/app/jsonp/getStatsData",
            id="getStatsData-JSONP",
        ),
        pytest.param(
            "refDataset",
            "xml",
            "https://api.e-stat.go.jp/rest/3.0/app/refDataset",
            id="refDataset-xml",
        ),
        pytest.param(
            "getDataCatalog",
            "json",
            "https://api.e-stat.go.jp/rest/3.0/app/json/getDataCatalog",
            id="getDataCalalog-json",
        ),
        pytest.param(
            "getStatsDatas",
            "csv",
            "https://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsDatas",
            id="getStatsDatas-csv",
        ),
    ],
)


class TestEndpoint:
    def test_netloc(self):
        assert _endpoint.Endpoint.netloc == "api.e-stat.go.jp"

    @pytest.mark.parametrize(*test_data_build)
    def test_build(self, api_type, response_data_type, expected):
        built_endpoint = _endpoint.Endpoint(api_type, response_data_type).build()
        assert built_endpoint == expected
