from covid_19.api import (
    get_all,
    countries,
    states,
    for_date,
)


def test_get_all():
    get_all()

    state = "California"

    california_records = get_all(state=state)

    assert all(r["state"] == state for r in california_records)


def test_countries():
    countries()


def test_states():
    states()


def test_for_date():
    for_date()
