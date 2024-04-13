import re
from typing import Annotated, Literal

import requests
from pydantic import Field, ValidationError, validate_call

from estatapi import _appid, _endpoint, _enum

YearsStr = Field(
    default=None,
    pattern=r"^(?:\d{4}|\d{4}(0[1-9]|1[0-2])|\d{4}(0[1-9]|1[0-2])-\d{4}(0[1-9]|1[0-2]))$",
)

StatsField = Field(
    default=None,
    pattern=r"^(?:\d{2}|\d{4})?$",
)

StatsCode = Field(
    default=None,
    pattern=r"^(?:\d{5}|\d{8})?$",
)

DateStr = Field(
    default=None,
    pattern=r"^(?:\d{4}|\d{4}(0[1-9]|1[0-2])|\d{4}(0[1-9]|1[0-2])([0-2][1-9]|3[0-1])|\d{4}(0[1-9]|1[0-2])([0-2][1-9]|3[0-1])-\d{4}(0[1-9]|1[0-2])([0-2][1-9]|3[0-1]))$",
)


@validate_call
def get_stats_list(
    surveyYears: str | None = YearsStr,
    openYears: str | None = YearsStr,
    statsField: str | None = StatsField,
    statsCode: str | None = StatsCode,
    searchWord: str | None = None,
    searchKind: Literal["1", "2"] = "1",
    collectArea: Literal["1", "2", "3"] | None = None,
    explanationGetFlg: Literal["Y", "N"] = "Y",
    statsNameList: Literal["Y"] | None = None,
    startPosition: int | None = Field(default=None, ge=1),
    limit: int | None = Field(default=None, ge=1),
    updatedDate: str | None = DateStr,
    lang: Literal["J", "E"] = Field(default="J"),
) -> requests.Response:
    """
    統計表情報取得
    -------------

    Parameters
    ----------
    `surveyYears` : str, optional
        調査年月。
        - 'yyyy': 単年検索
        - 'yyyymm': 単月検索
        - 'yyyymm-yyyymm': 範囲検索

    `openYears` : str, optional
        公開年月。
        - 'yyyy': 単年検索
        - 'yyyymm': 単月検索
        - 'yyyymm-yyyymm': 範囲検索

    `statsField` : str, optional
        統計分野。
        - 数値2桁: 統計大分類で検索
        - 数値4桁: 統計小分類で検索

        詳しくは以下のURL参照。
        https://www.e-stat.go.jp/api/api-info/statsfield

    `statsCode` : str, optional
        政府統計コード。
        - 数値5桁: 作成期間で検索
        - 数値8桁: 政府統計コードで検索

        詳しくは以下のURL参照。
        https://www.e-stat.go.jp/help/stat-search-3-5

    `searchWord` : str, optional
        検索キーワード。
        任意の文字列を指定します。

        表題やメタ情報等に含まれている文字列を検索します。
        AND、OR 又は NOT を指定して複数ワードでの検索が可能です。 (東京 AND 人口、東京 OR 大阪 等)

    `searchKind` : str, default '1'
        検索データ種別。
        - '1': 統計情報
        - '2': 小地域・地域メッシュ

    `collectArea` : str, optional
        集計地域区分。
        - '1': 全国
        - '2': 都道府県
        - '3': 市区町村

        検索データ種別=2（小地域・地域メッシュ）の場合は、無効になります。

    `explanationGetFlg` : Literal['Y', 'N'], default 'Y'
        解説情報有無。
        統計表及び、提供統計、提供分類の解説を取得するか否かを以下のいずれかから指定して下さい。
        - Y: 取得する
        - N: 取得しない

    `statsNameList`: Literal['Y'] , optional
        統計表情報でなく、統計調査名の一覧を取得する場合に指定して下さい。
        - Y: 統計調査名一覧

        `statsNameList` パラメータを省略した場合は統計表情報を出力します。

    `startPosition` : int, optional
        データ取得開始位置。

        データの取得開始位置（1から始まる行番号）を指定して下さい。省略時は先頭から取得します。
        統計データを複数回に分けて取得する場合等、継続データを取得する開始位置を指定するために指定します。
        前回受信したデータの<NEXT_KEY>タグの値を指定します。

    `limit` : int , optional
        データ取得件数。

        データの取得行数を指定して下さい。省略時は10万件です。
        データ件数が指定したlimit値より少ない場合、全件を取得します。データ件数が指定したlimit値より多い場合（継続データが存在する）は、受信したデータの<NEXT_KEY>タグに継続データの開始行が設定されます。

    `updatedDate` : str , optional
        更新日付。

        更新日付を指定します。指定された期間で更新された統計表の情報を提供します。
        以下のいずれかの形式で指定して下さい。
        - yyyy：単年検索
        - yyyymm：単月検索
        - yyyymmdd：単日検索
        - yyyymmdd-yyyymmdd：範囲検索

    `lang` : Literal['J', 'E'], default 'J'
        取得するデータの言語。
        - 'J': 日本語
        - 'E': 英語

    Returns
    -------
    api_response : requests.Response
    """

    params = {
        "lang": lang,
        "surveyYears": surveyYears,
        "openYears": openYears,
        "statsField": statsField,
        "statsCode": statsCode,
        "searchWord": searchWord,
        "searchKind": searchKind,
        "collectArea": collectArea,
        "explanationGetFlg": explanationGetFlg,
        "statsNameList": statsNameList,
        "startPosition": startPosition,
        "limit": limit,
        "updatedDate": updatedDate,
    }

    # check if APP ID is set
    _appid._check_appid()
    params["appId"] = _appid.get_appid()

    # build endpoint
    endpoint = _endpoint.Endpoint(
        api_type=_enum.ApiType.getStatsList,
        response_data_type=_enum.ResponseDataType.JSON,
    ).build()

    # get response
    response = requests.get(url=endpoint, params=params)

    return response


@validate_call
def get_meta_info(
    statsDataId: str,
    explanationGetFlg: Literal["Y", "N"] = "Y",
    lang: Literal["J", "E"] = Field(default="J"),
) -> requests.Response:
    """
    メタ情報取得
    -------------

    Parameters
    ----------
    `statsDataId` : str
        統計表ID。

       「統計表情報取得」で得られる統計表IDです。

    `explanationGetFlg` : Literal['Y', 'N'], default 'Y'
        解説情報有無。

        統計表及び、提供統計、提供分類、各事項の解説を取得するか否かを以下のいずれかから指定して下さい。
        - Y: 取得する (省略値)
        - N: 取得しない

    `lang` : Literal['J', 'E'], default 'J'
        取得するデータの言語。
        - 'J': 日本語
        - 'E': 英語

    Returns
    -------
    api_response : requests.Response
    """

    params = {
        "statsDataId": statsDataId,
        "explanationGetFlg": explanationGetFlg,
        "lang": lang,
    }

    # check if APP ID is set
    _appid._check_appid()
    params["appId"] = _appid.get_appid()

    # build endpoint
    endpoint = _endpoint.Endpoint(
        api_type=_enum.ApiType.getMetaInfo,
        response_data_type=_enum.ResponseDataType.JSON,
    ).build()

    # get response
    response = requests.get(url=endpoint, params=params)

    return response


def _validate_dataSetId_statsDataId(dataSetId, statsDataId):
    if (dataSetId is None) ^ (statsDataId is None):
        return
    else:
        message = (
            "Only one of dataSetId and statsDataId must be specified"
            "\n"
            f"dataSetId={dataSetId}, statsDataId={statsDataId}"
        )
        raise ValueError(message)


def _validate_kwargs(kwargs: dict):
    pattern = r"(^(lvCat|cdCat)(0[2-9]|1[0-5])$|^cdCat(0[2-9]|1[0-5])(From|To)$)"
    prog = re.compile(pattern)

    not_match = [prog.match(key) is None for key in kwargs.keys()]

    if any(not_match):
        message = "Names of arguments are invalid." "\n" f"{list(kwargs.keys())}"
        raise ValueError(message)


@validate_call
def get_stats_data(
    dataSetId: str | None = None,
    statsDataId: str | None = None,
    lvTab: str | None = None,
    cdTab: str | None = None,
    cdTabFrom: str | None = None,
    cdTabTo: str | None = None,
    lvTime: str | None = None,
    cdTime: str | None = None,
    cdTimeFrom: str | None = None,
    cdTimeTo: str | None = None,
    lvArea: str | None = None,
    cdArea: str | None = None,
    cdAreaFrom: str | None = None,
    cdAreaTo: str | None = None,
    lvCat01: str | None = None,
    cdCat01: str | None = None,
    cdCat01From: str | None = None,
    cdCat01To: str | None = None,
    startPosition: int | None = Field(default=None, ge=1),
    limit: int | None = Field(default=None, ge=1),
    metaGetFlg: Literal["Y", "N"] = "Y",
    cntGetFlg: Literal["Y", "N"] = "N",
    explanationGetFlg: Literal["Y", "N"] = "Y",
    annotationGetFlg: Literal["Y", "N"] = "Y",
    replaceSpChar: Literal[0, 1, 2, 3] = 0,
    lang: Literal["J", "E"] = Field(default="J"),
    **kwargs: Annotated[str, Field(...)],
) -> requests.Response:
    """
    統計データ取得
    -------------

    詳しくは以下のurlを参照
    https://www.e-stat.go.jp/api/api-info/e-stat-manual3-0#api_3_4

    Parameters
    ----------
    `dataSetId` : str, optional
        データセットID。

        「データセット登録」で登録したデータセットID です。

    `statsDataId` : str, optional
        統計表ID。

        「統計表情報取得」で得られる統計表IDです。

    `lvTab` : str, optional
        絞り込み条件 - 表章事項 - 階層レベル。

        以下のいずれかの形式で指定して下さい。
        (Xは「メタ情報取得」で得られる各メタ情報の階層レベル)
        - 'X'   :指定階層レベルのみで絞り込み
        - 'X-X' :指定階層レベルの範囲で絞り込み
        - '-X'  :階層レベル1 から指定階層レベルの範囲で絞り込み
        - 'X-'  :指定階層レベルから階層レベル 9 の範囲で絞り込み

    `cdTab` : str, optional
        絞り込み条件 - 表章事項 - 単一コード。

        特定の項目コードでの絞り込み
        「メタ情報取得」で得られる各メタ情報の項目コードを指定して下さい。
        コードはカンマ区切りで100個まで指定可能です。

    `cdTabFrom` : str, optional
        絞り込み条件 - 表章事項 - コードFrom。

        項目コードの範囲で絞り込み
        絞り込む範囲の開始位置の項目コードを指定して下さい。

    `cdTabTo` : str, optional
        絞り込み条件 - 表章事項 - コードTo。

        項目コードの範囲で絞り込み
        絞り込む範囲の終了位置の項目コードを指定して下さい。

    `lvTime` : str, optional
        絞り込み条件 - 時間軸事項 - 階層レベル。

        表章事項の階層レベル(`lvTab`)と同様です。

    `cdTime` : str, optional
        絞り込み条件 - 時間軸事項 - 単一コード。

        表章事項の単一コード(`cdTab`)と同様です。

    `cdTimeFrom` : str, optional
        絞り込み条件 - 時間軸事項 - コードFrom。

        表章事項のコードFrom(`cdTabFrom`)と同様です。

    `cdTimeTo` : str, optional
        絞り込み条件 - 時間軸事項 - コードTo。

        表章事項のコードTo(`cdTabTo`)と同様です。

    `lvArea` : str, optional
        絞り込み条件 - 地域事項 - 階層レベル。

        表章事項の階層レベル(`lvTab`)と同様です。

    `cdArea` : str, optional
        絞り込み条件 - 地域事項 - 単一コード。

        表章事項の単一コード(`cdTab`)と同様です。

    `cdAreaFrom` : str, optional
        絞り込み条件 - 地域事項 - コードFrom。

        表章事項のコードFrom(`cdTabFrom`)と同様です。

    `cdAreaTo` : str, optional
        絞り込み条件 - 地域事項 - コードTo。

        表章事項のコードTo(`cdTabTo`)と同様です。

    `lvCat01` : str, optional
        絞り込み条件 - 分類事項01 - 階層レベル。

        表章事項の階層レベル(`lvTab`)と同様です。

    `cdCat01` : str, optional
        絞り込み条件 - 分類事項01 - 単一コード。

        表章事項の単一コード(`cdTab`)と同様です。

    `cdCat01From` : str, optional
        絞り込み条件 - 分類事項01 - コードFrom。

        表章事項のコードFrom(`cdTabFrom`)と同様です。

    `cdCat01To` : str, optional
        絞り込み条件 - 分類事項01 - コードTo。

        表章事項のコードTo(`cdTabTo`)と同様です。

    `startPosition` : int, optional
        データ取得開始位置。

        データの取得開始位置（1から始まる行番号）を指定して下さい。省略時は先頭から取得します。
        統計データを複数回に分けて取得する場合等、継続データを取得する開始位置を指定するために指定します。
        前回受信したデータの<NEXT_KEY>タグの値を指定します。

    `limit` : int , optional
        データ取得件数。

        データの取得行数を指定して下さい。省略時は10万件です。
        データ件数が指定したlimit値より少ない場合、全件を取得します。データ件数が指定したlimit値より多い場合（継続データが存在する）は、受信したデータのタグに継続データの開始行が設定されます。

    `metaGetFlg` : Literal['Y', 'N'], default 'Y'
        メタ情報有無。

        統計データと一緒にメタ情報を取得するか否かを以下のいずれかから指定して下さい。
        - Y: 取得する
        - N: 取得しない

    `cntGetFlg` : Literal['Y', 'N'], default 'N'
        件数取得フラグ。

        指定した場合、件数のみ取得できます。`metaGetFlg`=Yの場合は、メタ情報も同時に返却されます。
        - Y: 件数のみ取得する。統計データは取得しない。
        - N: 件数及び統計データを取得する。(省略値)

    `explanationGetFlg` : Literal['Y', 'N'], default 'Y'
        解説情報有無。

        統計表及び、提供統計、提供分類の解説を取得するか否かを以下のいずれかから指定して下さい。
        - Y: 取得する
        - N: 取得しない

    `annotationGetFlg` : Literal['Y', 'N'], default 'Y'
        注釈情報有無。

        数値データの注釈を取得するか否かを以下のいずれかから指定して下さい。
        - Y: 取得する
        - N: 取得しない

    `replaceSpChar` : Literal[0, 1, 2, 3], default 0
        特殊文字の置換。

        特殊文字を置換するか否かを設定します。
        - 0: 置換しない（デフォルト）
        - 1: 0（ゼロ）に置換する
        - 2: NULL（長さ0の文字列、空文字)に置換する
        - 3:  NA（文字列）に置換する

    `lang` : Literal['J', 'E'], default 'J'
        取得するデータの言語。
        - 'J': 日本語
        - 'E': 英語

    Returns
    -------
    api_response : requests.Response
    """
    # check if only one of dataSetId and statsDataId is specified
    _validate_dataSetId_statsDataId(dataSetId, statsDataId)

    # check if keys of kwargs are valid
    _validate_kwargs(kwargs)

    params = {
        "dataSetId": dataSetId,
        "statsDataId": statsDataId,
        "lvTab": lvTab,
        "cdTab": cdTab,
        "cdTabFrom": cdTabFrom,
        "cdTabTo": cdTabTo,
        "lvTime": lvTime,
        "cdTime": cdTime,
        "cdTimeFrom": cdTimeFrom,
        "cdTimeTo": cdTimeTo,
        "lvArea": lvArea,
        "cdArea": cdArea,
        "cdAreaFrom": cdAreaFrom,
        "cdAreaTo": cdAreaTo,
        "lvCat01": lvCat01,
        "cdCat01": cdCat01,
        "cdCat01From": cdCat01From,
        "cdCat01To": cdCat01To,
        "startPosition": startPosition,
        "limit": limit,
        "metaGetFlg": metaGetFlg,
        "cntGetFlg": cntGetFlg,
        "explanationGetFlg": explanationGetFlg,
        "annotationGetFlg": annotationGetFlg,
        "replaceSpChar": replaceSpChar,
        "lang": lang,
        **kwargs,
    }

    # check if APP ID is set
    _appid._check_appid()
    params["appId"] = _appid.get_appid()

    # build endpoint
    endpoint = _endpoint.Endpoint(
        api_type=_enum.ApiType.getStatsData,
        response_data_type=_enum.ResponseDataType.JSON,
    ).build()

    # get response
    response = requests.get(url=endpoint, params=params)

    return response
