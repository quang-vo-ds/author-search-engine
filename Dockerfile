FROM ubuntu:18.04
RUN apt-get -y update && apt -get install software-properties-common \
&& add-apt-repository ppa:deadsnakes/ppa && apt install python3.10

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt 

COPY ./model/   ./model/
COPY ./database_embedder/   ./database_embedder/
COPY ./app/app.py   ./
CMD ["app.handler"]