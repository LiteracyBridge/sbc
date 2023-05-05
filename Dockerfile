FROM python:3.8

COPY ./backend ./app

# COPY .//requirements.txt ./requirements.txt
RUN pip install -r ./app/requirements.txt

# WORKDIR /app


ENV HOST="0.0.0.0"
ENV PORT=5000

ENTRYPOINT uvicorn app.app:app --host ${HOST} --port ${PORT}
