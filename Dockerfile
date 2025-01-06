FROM python:3.13
LABEL authors="kolo"

WORKDIR /src

COPY poetry.lock pyproject.toml /src/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY . /src

CMD ["/bin/bash", "-c", "python main.py"]
