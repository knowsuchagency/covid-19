FROM python:3-slim

RUN apt-get update

RUN apt-get install -y build-essential

RUN mkdir /src

WORKDIR /src

RUN pip install -U pip

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY covid_19 /src/covid_19

COPY poetry.lock /src

COPY pyproject.toml /src

COPY README.md /src

RUN poetry install

CMD gunicorn --bind "0.0.0.0:80" --worker-class="egg:meinheld#gunicorn_worker" covid_19.api:__hug_wsgi__
