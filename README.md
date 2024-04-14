# estatapi-python

estatapi-pythonは [e\-StatのAPI機能](https://www.e-stat.go.jp/api/api-info)を扱うためのPythonパッケージです。

現在はAPI機能のうち、以下の機能をサポートしています。

1. 統計表情報取得（GET）
    - 統計表の情報（統計表ID、調査名、統計表名、調査年月等）を提供する機能。
    検索キーワード等を指定することで、絞込みが可能。
2. メタ情報取得（GET）
    - 統計表（統計表ID）に含まれるメタ情報（集計事項、地域事項、分類事項等）を提供する機能。
3. 統計データ取得（GET）
    - 統計表（統計表ID）に収録されている統計データ（数値データ）を提供する機能。
    必要に応じて、データセット、メタ情報による絞込みを行うことができる。
    提供するデータが大量の場合は、分割して提供される。


## インストール方法

```shell
pip install ...
```

## アプリケーションIDの取得

e-StatのAPI機能を利用するには、アプリケーションIDが必要です。

以下の利用ガイドから、ユーザ登録・アプリケーションIDの取得をお願いします。

[利用ガイド \| 政府統計の総合窓口\(e\-Stat\)−API機能](https://www.e-stat.go.jp/api/api-info/api-guide)

## 使用方法

### アプリケーションIDの設定

```python
>>> import estatapi
>>> # 取得したアプリケーションIDを設定する
>>> APPID = "YOUR_APPID"
>>> estatapi.set_appid(APPID)
```

### 統計表情報取得

```python
>>> from pprint import pprint
>>> # 統計表情報を取得する
>>> stats_list_response = estatapi.get_stats_list(limit=3, statsField="02")
>>> pprint(stats_list_response.json(), depth=3)
{'GET_STATS_LIST': {'DATALIST_INF': {'NUMBER': 19028,
                                     'RESULT_INF': {...},
                                     'TABLE_INF': [...]},
                    'PARAMETER': {'DATA_FORMAT': 'J',
                                  'EXPLANATION_GET_FLG': 'Y',
                                  'LANG': 'J',
                                  'LIMIT': 3,
                                  'SEARCH_KIND': 1,
                                  'STATS_FIELD': '02'},
                    'RESULT': {'DATE': '2024-04-14T09:01:46.136+09:00',
                               'ERROR_MSG': '正常に終了しました。',
                               'STATUS': 0}}}
>>> # 統計表情報をpandasデータフレームに変換する
>>> df_stats_list = estatapi.stats_list_to_pandas(stats_list_response.json())
>>> df_stats_list.head()
          @id        STATISTICS_NAME CYCLE  SURVEY_DATE   OPEN_DATE  
0  0000030001  昭和55年国勢調査 第1次基本集計 全国編     -       198010  2007-10-05   
1  0000030002  昭和55年国勢調査 第1次基本集計 全国編     -       198010  2007-10-05   
2  0000030003  昭和55年国勢調査 第1次基本集計 全国編     -       198010  2007-10-05   
```

### メタ情報取得

```python
>>> from pprint import pprint
>>> # メタ情報を取得する
>>> meta_info_response = estatapi.get_meta_info(statsDataId="0000030001")
>>> pprint(meta_info_response.json(), depth=3)
{'GET_META_INFO': {'METADATA_INF': {'CLASS_INF': {...}, 'TABLE_INF': {...}},
                   'PARAMETER': {'DATA_FORMAT': 'J',
                                 'EXPLANATION_GET_FLG': 'Y',
                                 'LANG': 'J',
                                 'STATS_DATA_ID': '0000030001'},
                   'RESULT': {'DATE': '2024-04-14T09:01:53.803+09:00',
                              'ERROR_MSG': '正常に終了しました。',
                              'STATUS': 0}}}
```


### 統計データ取得

```python
>>> from pprint import pprint
>>> # 統計データを取得する
>>> stats_data_response = estatapi.get_stats_data(statsDataId="0000030001")
>>> pprint(stats_data_response.json(), depth=3)
{'GET_STATS_DATA': {'PARAMETER': {'ANNOTATION_GET_FLG': 'Y',
                                  'CNT_GET_FLG': 'N',
                                  'DATA_FORMAT': 'J',
                                  'EXPLANATION_GET_FLG': 'Y',
                                  'LANG': 'J',
                                  'METAGET_FLG': 'Y',
                                  'START_POSITION': 1,
                                  'STATS_DATA_ID': '0000030001'},
                    'RESULT': {'DATE': '2024-04-14T09:01:57.299+09:00',
                               'ERROR_MSG': '正常に終了しました。',
                               'STATUS': 0},
                    'STATISTICAL_DATA': {'CLASS_INF': {...},
                                         'DATA_INF': {...},
                                         'RESULT_INF': {...},
                                         'TABLE_INF': {...}}}}
>>> # 統計データをpandasデータフレームに変換する
>>> df_stats_data = estatapi.stats_data_to_pandas(stats_data_response.json())
>>> df_stats_data.head()
  全域・集中の別030002 全域・集中の別030002_階層 男女Ａ030001 ...     値  
0            全域                1      男女総数            ...  117060396  
1            全域                1      男女総数            ...   89187409  
2            全域                1      男女総数            ...   27872987  
3            全域                1      男女総数            ...    5575989  
4            全域                1      男女総数            ...    1523907  
```

## クレジット

「このサービスは、政府統計総合窓口(e-Stat)のAPI機能を使用していますが、サービスの内容は国によって保証されたものではありません。」