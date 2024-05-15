FROM python:3.11.9

RUN mkdir /weather

WORKDIR /weather

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "app.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--build=0.0.0.0:8000"]