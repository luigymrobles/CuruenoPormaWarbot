FROM python:3.11

RUN mkdir -p /root
WORKDIR /root

RUN pip install poetry==1.6.1

COPY src /root/src
COPY poetry.lock /root/poetry.lock
COPY pyproject.toml /root/pyproject.toml
COPY README.md /root/README.md

RUN poetry config virtualenvs.create false
RUN poetry install

# Run the app
# CMD ["python", "main.py"]
# Docker dev env
CMD ["tail", "-f", "/dev/null"]
