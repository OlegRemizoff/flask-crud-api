# FROM python:3.10-slim

FROM python:alpine

RUN pip install --upgrade pip


WORKDIR /app

COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt
COPY . .
EXPOSE 5000


CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000"]



