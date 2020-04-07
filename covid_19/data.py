import datetime as dt
import io
from concurrent import futures

import pandas as pd
import requests

INITIAL_DATE = dt.date(2020, 1, 22)


def get_dataframe_for_date(date: dt.date = INITIAL_DATE) -> pd.DataFrame:
    """Fetch the appropriate csv from github and return it as a datafram."""

    url = (
        "https://raw.githubusercontent.com/"
        "CSSEGISandData/COVID-19/master/"
        "csse_covid_19_data/"
        "csse_covid_19_daily_reports/"
        "{date}.csv"
    ).format(date=date.strftime("%m-%d-%Y"))

    resp = requests.get(url)

    with io.StringIO(resp.text) as fp:
        return pd.read_csv(fp)


def get_dataframe(start_date=INITIAL_DATE, end_date=None) -> pd.DataFrame:
    """Fetch the appropriate csv(s) for a given daterange, concatenate them, and return a dataframe."""

    end_date = (
        end_date
        if end_date is not None
        else dt.datetime.utcnow() - dt.timedelta(days=1)
    ).date()

    dates = pd.date_range(start_date, end_date)

    with futures.ThreadPoolExecutor() as ex:

        df = pd.concat(ex.map(get_dataframe_for_date, dates))

    df.rename(columns=str.lower, inplace=True)

    df.drop(columns=[c for c in df.columns if "/" in c], inplace=True)

    df["datetime"] = pd.to_datetime(df["last_update"])

    df["date"] = df.datetime.map(lambda d: d.date())

    # df["county"] = df.admin2
    renames = {
        "country_region": "country",
        "province_state": "state",
        "admin2": "county",
    }

    df.rename(columns=renames, inplace=True)

    df.drop(
        columns=["last update", "last_update", "lat", "long_", "combined_key"],
        inplace=True,
    )

    return df
