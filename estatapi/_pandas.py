import dataclasses

import pandas as pd


def _get_value_mappers(class_obj):
    value_mappers = {}

    for obj in class_obj:
        class_ = obj["CLASS"]
        if isinstance(class_, dict):
            mapper = {class_["@code"]: class_["@name"]}
        elif isinstance(class_, list):
            mapper = {c["@code"]: c["@name"] for c in class_}
        value_mappers["@" + obj["@id"]] = mapper

    return value_mappers


def _get_level_mappers(class_obj):
    levels = {}

    for obj in class_obj:
        class_ = obj["CLASS"]
        if isinstance(class_, dict):
            value_mapper = {class_["@code"]: class_["@level"]}
        elif isinstance(class_, list):
            value_mapper = {c["@code"]: c["@level"] for c in class_}
        levels["@" + obj["@id"]] = value_mapper

    return levels


@dataclasses.dataclass
class StatisticalData:
    json_data: dict

    def _metainfo_exists(self) -> bool:
        """
        If json_data has metainfo ("CLASS_INF" key), this function returns True. Otherwise return False.
        """
        metainfo_exists = "CLASS_INF" in self.json_data
        return metainfo_exists

    def get_raw_df(self):
        df_value = pd.json_normalize(self.json_data["DATA_INF"]["VALUE"])
        return df_value

    def get_column_mapper(self, add_level: bool = True):
        class_obj = self.json_data["CLASS_INF"]["CLASS_OBJ"]
        mapper = {"@" + class_["@id"]: class_["@name"] for class_ in class_obj}
        if add_level:
            mapper.update(
                {k + "_level": mapper[k] + "_階層" for k in self.get_level_mappers()}
            )
        mapper.update({"@unit": "単位", "$": "値"})
        return mapper

    def get_value_mappers(self):
        return _get_value_mappers(self.json_data["CLASS_INF"]["CLASS_OBJ"])

    def get_level_mappers(self):
        return _get_level_mappers(self.json_data["CLASS_INF"]["CLASS_OBJ"])

    def to_df(self, add_level: bool = True):
        df = self.get_raw_df()

        # if metainfo is not provided, return raw df
        if not self._metainfo_exists():
            return df

        columns = []

        for col_name in df.columns:
            columns.append(col_name)
            if add_level and (
                (level_mapper := self.get_level_mappers().get(col_name)) is not None
            ):
                columns.append(col_name + "_level")
                # mapping levels
                df[col_name + "_level"] = df[col_name].map(level_mapper)
            if (value_mapper := self.get_value_mappers().get(col_name)) is not None:
                # mapping values
                df[col_name] = df[col_name].map(value_mapper)

        # reordering columns
        df = df.reindex(columns=columns)

        # renaming columns
        df = df.rename(columns=self.get_column_mapper())
        return df


def stats_data_to_pandas(stats_data_json: dict, add_level: bool = True) -> pd.DataFrame:
    stats_data = StatisticalData(stats_data_json["GET_STATS_DATA"]["STATISTICAL_DATA"])
    return stats_data.to_df(add_level=add_level)


def stats_list_to_pandas(stats_list_json: dict) -> pd.DataFrame:
    table_inf = stats_list_json["GET_STATS_LIST"]["DATALIST_INF"]["TABLE_INF"]
    df = pd.json_normalize(table_inf)
    return df


def to_pandas(json_data: dict) -> pd.DataFrame:
    """
    e-Stat APIのJSON形式のデータをpandasデータフレームに変換します。

    現在は `get_stats_list`と `get_stats_data` の出力に対応しています。

    Parameters
    ----------
    `json_data` : dict

    """
    to_pandas_function = {
        "GET_STATS_DATA": stats_data_to_pandas,
        "GET_STATS_LIST": stats_list_to_pandas,
    }

    root_key = list(json_data.keys())[0]

    return to_pandas_function[root_key](json_data)
