from enum import Enum


class ApiType(str, Enum):
    getStatsList = "getStatsList"
    getMetaInfo = "getMetaInfo"
    getStatsData = "getStatsData"
    # postDataset = "postDataset"
    refDataset = "refDataset"
    getDataCatalog = "getDataCatalog"
    getStatsDatas = "getStatsDatas"


class ResponseDataType(str, Enum):
    XML = "xml"
    JSON = "json"
    JSONP = "jsonp"
    CSV = "csv"
