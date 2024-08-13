FROM python:3.12-alpine

RUN mkdir /instruktor
WORKDIR /HelpDeskBot

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
