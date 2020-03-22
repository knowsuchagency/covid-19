from covid_19.api import (
    fetch,
    countries_and_regions,
    states_and_provinces,
    for_date,
)


def test_fetch():
    fetch()


def test_countries_and_regions():
    countries_and_regions()


def test_states_and_provinces():
    states_and_provinces()


def test_for_date():
    for_date()
