FROM python:3.8-slim AS telegram-bot

WORKDIR .

COPY ./src ./src

WORKDIR ./src

RUN pip install -r requirements.txt

CMD ["python", "./app.py"]
