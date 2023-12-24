FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt 

COPY ./model/   ./model/
COPY ./database_embedder/   ./database_embedder/
COPY ./app/app.py   ./
CMD ["app.handler"]