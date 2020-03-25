"""
This API is a wrapper around Johns Hopkins' https://github.com/CSSEGISandData/COVID-19 dataset.

Please abide by their terms of use with respect to how you use their data via this API.

You can find the source code at https://github.com/knowsuchagency/covid-19
"""

import datetime as dt
import json
import logging
import threading
from typing import *

import hug

from covid_19.data import get_dataframe
from covid_19.utils import to_records, expose
from covid_19.wsgi import StandaloneApplication

df = get_dataframe()


def update_df(period=86400):
    """Update the dataframe daily."""
    global df
    event = threading.Event()
    while not event.wait(period):
        logging.warning("updating the dataframe")
        df = get_dataframe()


threading.Thread(target=update_df, daemon=True).start()

api = hug.API(__name__)

api.name = "COVID-19 API"


@hug.get(
    examples=[
        "country=US&date=2020-03-20",
        "min_date=2020-02-01&state=California&limit=100",
    ],
)
@hug.cli(output=hug.output_format.pretty_json)
def get_all(
    date=None,
    country=None,
    state=None,
    min_date=None,
    max_date=None,
    countries=None,
    states=None,
    limit=None,
):
    """
    Fetch all data from John Hopkins.

    Args:

        date (str): iso-formatted date
        country (str): country or region
        state (str): state or province
        min_date: (str): iso-formatted date
        max_date (str): iso-formatted date
        countries List[str]: json-formatted array of strings
        states List[str]: json-formatted array of strings
        limit (int): the maximum number of rows to be returned

    """
    result = df

    if date is not None:
        from pprint import pprint

        print(f"date: {date}")
        print(list(date))
        result = df[
            df["Last Update"].map(lambda d: d.date())
            == dt.datetime.fromisoformat(date).date()
        ]

    if country is not None:
        result = result[result["Country/Region"] == country]

    if state is not None:
        result = result[result["Province/State"] == state]

    if min_date is not None:
        result = result[
            result["Last Update"].map(lambda d: d.date())
            >= dt.datetime.fromisoformat(min_date).date()
        ]

    if max_date is not None:
        result = result[
            result["Last Update"].map(lambda d: d.date())
            <= dt.datetime.fromisoformat(max_date).date()
        ]

    if countries is not None:
        countries = (
            json.loads(countries)
            if not isinstance(countries, list)
            else countries
        )
        result = result[
            result["Countries/Regions"].map(lambda s: s in countries)
        ]

    if states is not None:
        states = json.loads(states) if not isinstance(states, list) else states
        result = result[result["Province/State"].map(lambda s: s in states)]

    records = to_records(result)

    if limit is not None:
        records = records[: int(limit)]

    return records


@expose
def countries():
    """Return all countries and regions in the dataset."""
    return df["Country/Region"].to_list()


@expose
def states():
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
    options = {
        "bind": f"{host}:{port}",
        "worker-class": "egg:meinheld#gunicorn_worker",
    }
    StandaloneApplication(__hug_wsgi__, options).run()


if __name__ == "__main__":
    api.cli()
