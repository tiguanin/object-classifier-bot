FROM python:3.8-slim AS object-classifier

WORKDIR .

COPY ./src ./src

WORKDIR ./src

RUN pip install -r requirements.txt

RUN ["sh", "./entrypoint.sh"]
CMD ["python", "./app.py"]
