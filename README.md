# COVID-19 API

**[coronavirus-api.net][coronavirus-api]**

![](https://github.com/knowsuchagency/covid-19/workflows/black/badge.svg)
![](https://github.com/knowsuchagency/covid-19/workflows/unit%20tests/badge.svg)

This API is a wrapper around Johns Hopkins' https://github.com/CSSEGISandData/COVID-19 dataset.

Please abide by their terms of use with respect to how you use their data via this API.

## Installation

This package is hosted on [pypi](https://pypi.org/project/covid-19/)

The recommended method of installation is through [pipx].
```bash
pipx install covid-19
```
However, covid-19 can also be pip-installed as normal.
```bash
pip install covid-19
```

## Website

The [coronavirus api website](https://coronavirus-api.net/get_all?min_date=2020-02-01&state=California&limit=100) allows several methods of slicing and dicing the data.

For example, the `get_all` endpoint (which returns all data) can be filtered for rows which only contain
data for California and Colorado as of March 22nd in this way:

`https://coronavirus-api.net/get_all?min_date=2020-03-22&states=["California", "Colorada"]`

The [main page][coronavirus-api] will list the available endpoints and their available parameters.

## CLI Usage

This package installs a command-line tool, `covid`

It lets you programmatically access John Hopkins' dataset via terminal commands
or via a rest api that can itself be instantiated locally from the cli

```bash
covid --help

This API is a wrapper around Johns Hopkins' https://github.com/CSSEGISandData/COVID-19 dataset.

Please abide by their terms of use with respect to how you use their data via this API.


Available Commands:

 - get_all: Fetch all data from John Hopkins.
 - countries: Return all countries and regions in the dataset.
 - states: Return all states and provinces in the dataset.
 - for_date: Return all data for a specific date.
 - serve: Serve REST API locally.

```

i.e.

```bash
covid for_date 2020-03-21
[
    {
        "Province/State": "Hubei",
        "Country/Region": "China",
        "Last Update": "2020-03-22T09:43:06",
        "Confirmed": 67800.0,
        "Deaths": 3144.0,
        "Recovered": 59433.0,
        "Latitude": 30.9756,
        "Longitude": 112.2707
...
```

## Docker

This package can also be run as a [docker image][docker image].

```bash
docker run knowsuchagency/covid-19 --help
```

[pipx]: https://github.com/pipxproject/pipx
[coronavirus-api]: https://coronavirus-api.net
[docker image]: https://hub.docker.com/repository/docker/knowsuchagency/covid-19
