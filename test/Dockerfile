FROM python:3.8

RUN mkdir /code
WORKDIR /code

COPY requirements.txt requirements.txt

RUN apt-get update &&\
    pip install --upgrade pip &&\
    pip install -r requirements.txt

COPY  . .

ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["python", "test.py"]