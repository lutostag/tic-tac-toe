FROM python:3.7

WORKDIR /opt/tictactoe

COPY requirements.txt .

RUN pip install gunicorn psycopg2 -r requirements.txt

COPY . .

ENV GUNICORN_CMD_ARGS="-w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80"

CMD gunicorn tictactoe.backend.main:app
