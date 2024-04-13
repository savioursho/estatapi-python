from enum import StrEnum


class ApiType(StrEnum):
    getStatsList = "getStatsList"
    getMetaInfo = "getMetaInfo"
    getStatsData = "getStatsData"
    # postDataset = "postDataset"
    refDataset = "refDataset"
    getDataCatalog = "getDataCatalog"
    getStatsDatas = "getStatsDatas"


class ResponseDataType(StrEnum):
    XML = "xml"
    JSON = "json"
    JSONP = "jsonp"
    CSV = "csv"
