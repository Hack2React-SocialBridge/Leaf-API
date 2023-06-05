FROM python:3.11

WORKDIR /src

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY src/poetry.lock .
COPY src/pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root

COPY docker/python/entrypoint.sh /entrypoint.sh

RUN chmod 700 /entrypoint.sh

COPY src/ .

CMD ["/entrypoint.sh"]