from covid_19.api import (
    fetch,
    countries,
    states,
    for_date,
)


def test_fetch():
    fetch()


def test_countries():
    countries()


def test_states():
    states()


def test_for_date():
    for_date()
