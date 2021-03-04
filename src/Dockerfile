FROM python:3.8-slim as object-classifier

WORKDIR .

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./classifier.py"]