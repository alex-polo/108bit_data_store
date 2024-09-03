FROM python:3.12-alpine

RUN mkdir /data_bank
WORKDIR /data_bank

#COPY ../_requirements.txt .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#COPY scripts/*.sh .
#RUN chmod a+x ./scripts/*.sh
#RUN chmod a+x *.sh

CMD gunicorn src.server:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000