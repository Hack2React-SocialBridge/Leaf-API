FROM python:3.11

WORKDIR /src

RUN apt-get update

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

COPY src/poetry.lock .
COPY src/pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-root

COPY ./docker/python/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh


COPY ./docker/python/entrypoint-celeryworker.sh /entrypoint-celeryworker.sh
RUN sed -i 's/\r$//g' /entrypoint-celeryworker.sh
RUN chmod +x /entrypoint-celeryworker.sh

COPY ./docker/python/entrypoint-celerybeat.sh /entrypoint-celerybeat.sh
RUN sed -i 's/\r$//g' /entrypoint-celerybeat.sh
RUN chmod +x /entrypoint-celerybeat.sh

COPY ./docker/python/entrypoint-flower.sh /entrypoint-flower.sh
RUN sed -i 's/\r$//g' /entrypoint-flower.sh
RUN chmod +x /entrypoint-flower.sh

COPY src/ .

CMD ["/entrypoint.sh"]