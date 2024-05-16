FROM python:3.11.9

RUN mkdir /weather

WORKDIR /weather

COPY requirements.txt .
COPY cities.json .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /weather/docker/*.sh