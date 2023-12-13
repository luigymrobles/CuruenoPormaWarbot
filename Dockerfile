FROM python:3.11

RUN mkdir -p /src
WORKDIR /src

RUN pip install poetry==1.6.1
RUN poetry config virtualenvs.create false

COPY poetry.lock /src/poetry.lock
COPY pyproject.toml /src/pyproject.toml

RUN poetry install

COPY curueno_porma_warbot /src/curueno_porma_warbot
COPY README.md /src/README.md
COPY run_api.sh /src/run_api.sh

# Run the app
# CMD ["python", "main.py"]
# Docker dev env
CMD ["tail", "-f", "/dev/null"]
