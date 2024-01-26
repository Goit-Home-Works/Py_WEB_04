FROM python:3.11-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . .

COPY pyproject.toml poetry.lock $APP_HOME/
RUN pip install poetry

RUN poetry install 
RUN pip install Jinja2
RUN pip install python-dotenv

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

EXPOSE 3005

CMD ["python", "main.py"]