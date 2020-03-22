# COVID-19 API

This API is a wrapper around Johns Hopkins' https://github.com/CSSEGISandData/COVID-19 dataset.

Please abide by their terms of use with respect to how you use their data via this API.

## Installation

The recommended method of installation is through [pipx].
```bash
pipx install covid-19
```
However, covid-19 can also be pip-installed as normal.
```bash
pip install covid-19
```

## Usage

This package installs a command-line tool, `covid`

This tool lets you programmatically access John Hopkins' dataset in the terminal
but also lets you host a REST API for the data on your machine via the `serve` subcommand
i.e. `covid serve`

[pipx]: https://github.com/pipxproject/pipx
