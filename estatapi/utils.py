import pandas as pd


def list_stats_field() -> pd.DataFrame:
    url = "https://www.e-stat.go.jp/api/sites/default/files/uploads/2015/11/statsfield.csv"
    df = pd.read_csv(url, encoding="shift-jis", dtype=str)
    return df
