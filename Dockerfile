FROM python:3.8-slim

WORKDIR /code

RUN apt-get -y update --fix-missing
RUN apt-get -y install apt-utils
RUN apt-get -y dist-upgrade
RUN apt-get -y install gcc

RUN apt-get -y clean
COPY . /code

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "src/main.py"]