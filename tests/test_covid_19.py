from covid_19.api import (
    all,
    countries,
    states,
    for_date,
)


def test_all():
    all()

    state = "California"

    california_records = all(state=state)

    assert all(r["Province/State"] == state for r in california_records)


def test_countries():
    countries()


def test_states():
    states()


def test_for_date():
    for_date()
