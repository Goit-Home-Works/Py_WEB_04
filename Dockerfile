FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml $APP_HOME/

RUN pip install poetry

RUN poetry install --no-interaction --no-ansi

RUN pip install jinja2

COPY . .

CMD ["python", "main.py"]
