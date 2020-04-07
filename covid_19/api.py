"""This API is a wrapper around Johns Hopkins' https://github.com/CSSEGISandData/COVID-19 dataset."""

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


def update_df():
    """Update the dataframe every six hours by default."""
    global df
    event = threading.Event()
    while not event.wait(21600):
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
    county=None,
    counties=None,
    limit=None,
):
    """Fetch all data from John Hopkins."""

    result = df

    if date is not None:

        result = df[
            df.datetime.map(lambda d: d.date())
            == dt.datetime.fromisoformat(date).date()
        ]

    if min_date is not None:
        result = result[
            result["datetime"].map(lambda d: d.date())
            >= dt.datetime.fromisoformat(min_date).date()
        ]

    if max_date is not None:
        result = result[
            result["datetime"].map(lambda d: d.date())
            <= dt.datetime.fromisoformat(max_date).date()
        ]

    assert not (
        country and countries
    ), "country and countries filters are mutually exclusive"

    if country or countries:
        countries = (
            [country]
            if country
            else (
                json.loads(countries)
                if not isinstance(countries, list)
                else countries
            )
        )

        result = result[result.country.map(lambda c: c in countries)]

    assert not (
        state and states
    ), "state and states filters are mutually exclusive"

    if state or states:
        states = (
            [state]
            if state
            else json.loads(states)
            if not isinstance(states, list)
            else states
        )

        result = result[result.state.map(lambda s: s in states)]

    assert not (
        county and counties
    ), "county and counties filters are mutually exclusive"

    if county or counties:
        counties = (
            [county]
            if county
            else json.loads(counties)
            if not isinstance(counties, list)
            else counties
        )

        result = result[result.county.map(lambda c: c in counties)]

    records = to_records(result)

    if limit is not None:
        records = records[: int(limit)]

    return records


@expose
def counties():
    """Return all US counties in the dataset."""
    return df[df.country == "US"].county.dropna().unique().tolist()


@expose
def countries():
    """Return all countries and regions in the dataset."""
    return df.country.dropna().unique().tolist()


@expose
def states():
    """Return all states and provinces in the dataset."""
    return to_records(df[["state", "country"]].dropna())


@expose
def for_date(date_string=None):
    """Return all data for a specific date."""
    date_string: Optional[str]

    date = (
        dt.datetime.fromisoformat(date_string).date()
        if date_string is not None
        else (dt.datetime.utcnow() - dt.timedelta(days=1)).date()
    )

    result = df[df.datetime.map(lambda d: d.date()) == date]

    return to_records(result)


@hug.cli()
def serve(host: str = "", port: int = 80):
    """Serve REST API locally."""
    StandaloneApplication(__hug_wsgi__, bind=f"{host}:{port}").run()


if __name__ == "__main__":
    api.cli()
