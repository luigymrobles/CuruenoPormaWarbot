FROM python:3.11

RUN mkdir -p /src
WORKDIR /src

RUN pip install poetry==1.6.1

COPY curueno_porma_warbot /src/curueno_porma_warbot
COPY poetry.lock /src/poetry.lock
COPY pyproject.toml /src/pyproject.toml
COPY README.md /src/README.md

RUN poetry config virtualenvs.create false
RUN poetry install

# Run the app
# CMD ["python", "main.py"]
# Docker dev env
CMD ["tail", "-f", "/dev/null"]
