from covid_19.api import (
    fetch,
    countries,
    states,
    for_date,
)


def test_fetch():
    fetch()

    state = "California"

    california_records = fetch(state=state)

    assert all(r["Province/State"] == state for r in california_records)


def test_countries():
    countries()


def test_states():
    states()


def test_for_date():
    for_date()
