import dataclasses
import os.path
import urllib.parse

from estatapi._enum import ApiType, ResponseDataType


@dataclasses.dataclass
class Endpoint:
    netloc = "api.e-stat.go.jp"

    api_type: ApiType
    response_data_type: ResponseDataType
    scheme: str = "https"
    version: str = "3.0"

    def build(self) -> str:
        path = _build_path(
            api_type=self.api_type, response_data_type=self.response_data_type
        )
        url_tuple = (self.scheme, self.netloc, path, "", "", "")
        return urllib.parse.urlunparse(url_tuple)


def _build_path(
    api_type: ApiType,
    response_data_type: ResponseDataType,
    version: str = "3.0",
):
    api_type, response_data_type = _validate_types(api_type, response_data_type)

    path_list = ["rest", version, "app"]

    # response data type
    response_data_type_mapper = {
        ResponseDataType.XML: "",
        ResponseDataType.JSON: "json",
        ResponseDataType.JSONP: "jsonp",
        ResponseDataType.CSV: "",
    }
    path_list.append(response_data_type_mapper[response_data_type])

    # api type
    path_list.append(
        api_type.replace("get", "getSimple")
        if response_data_type == ResponseDataType.CSV
        else api_type
    )

    return os.path.join(*path_list)


def _validate_types(
    api_type: ApiType,
    response_data_type: ResponseDataType,
):
    api_type = ApiType[api_type]
    response_data_type = ResponseDataType[response_data_type.upper()]

    allowed_response_data_type = {
        ApiType.getStatsList: [
            ResponseDataType.XML,
            ResponseDataType.JSON,
            ResponseDataType.JSONP,
            ResponseDataType.CSV,
        ],
        ApiType.getMetaInfo: [
            ResponseDataType.XML,
            ResponseDataType.JSON,
            ResponseDataType.JSONP,
            ResponseDataType.CSV,
        ],
        ApiType.getStatsData: [
            ResponseDataType.XML,
            ResponseDataType.JSON,
            ResponseDataType.JSONP,
            ResponseDataType.CSV,
        ],
        ApiType.refDataset: [
            ResponseDataType.XML,
            ResponseDataType.JSON,
            ResponseDataType.JSONP,
        ],
        ApiType.getDataCatalog: [
            ResponseDataType.XML,
            ResponseDataType.JSON,
            ResponseDataType.JSONP,
        ],
        ApiType.getStatsDatas: [
            ResponseDataType.XML,
            ResponseDataType.JSON,
            ResponseDataType.CSV,
        ],
    }

    if response_data_type in allowed_response_data_type[api_type]:
        return api_type, response_data_type
    else:
        raise ValueError("This combination of types is not allowed.")
