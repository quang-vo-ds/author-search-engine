FROM ubuntu:22.04

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt 

COPY ./model/   ./model/
COPY ./database_embedder/   ./database_embedder/
COPY ./app/app.py   ./
CMD ["app.handler"]