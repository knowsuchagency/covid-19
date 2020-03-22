"""
This API is a wrapper around Johns Hopkins' https://github.com/CSSEGISandData/COVID-19 dataset.

Please abide by their terms of use with respect to how you use their data via this API.
"""

import datetime as dt
from typing import *

import hug

from covid_19.fetch import get_data
from covid_19.utils import to_records, expose

api = hug.API(__name__)

api.name = "Corona API"

api.cli.output_format = hug.output_format.pretty_json

api.http.output_format = hug.output_format.pretty_json

df = get_data()


@hug.get(examples=["country=US&date=2020-03-20"])
@hug.cli()
def fetch(date=None, country=None, state=None):
    """Fetch all data from John Hopkins."""
    result = df

    if date is not None:
        date = dt.datetime.fromisoformat(date).date()
        result = df[df["Last Update"].map(lambda d: d.date()) == date]

    if country is not None:
        result = result[result["Country/Region"] == country]

    if state is not None:
        result = result[result["Province/State"] == state]

    return to_records(result)


@expose
def countries_and_regions():
    """Return all countries and regions in the dataset."""
    return df["Country/Region"].to_list()


@expose
def states_and_provinces():
    """Return all states and provinces in the dataset."""
    return to_records(
        df[["Province/State", "Country/Region"]].dropna(how="any")
    )


@expose
def for_date(date_string=None):
    """Return all data for a specific date."""
    date_string: Optional[str]

    date = (
        dt.datetime.fromisoformat(date_string).date()
        if date_string is not None
        else (dt.datetime.utcnow() - dt.timedelta(days=1)).date()
    )

    result = df[df["Last Update"].map(lambda d: d.date()) == date]

    return to_records(result)


@hug.cli()
def serve(host: str = "", port: int = 80):
    """Serve REST API locally."""
    api.http.serve(host=host, port=port)


if __name__ == "__main__":
    api.cli()
