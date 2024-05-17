FROM python:3.11.9

RUN mkdir /weather

WORKDIR /weather

COPY requirements.txt .
COPY cities.json .

RUN pip install -r requirements.txt

COPY . .

# Если юзаем только dockerfile без docker-compose
RUN alembic upgrade head

CMD gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000