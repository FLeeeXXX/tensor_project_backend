FROM python:3.11.9

RUN mkdir /weather

WORKDIR /weather

COPY requirements.txt .
COPY cities.json .

RUN pip install -r requirements.txt

COPY . .

WORKDIR app

RUN alembic upgrade head

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000