FROM ubuntu:latest



RUN apt-get update
RUN apt-get install -y openjdk-8-jdk
RUN apt-get update
RUN apt-get install git -y
RUN apt-get update
RUN apt-get install wget -y

COPY main.py /
COPY use_case /use_case
COPY service /service


RUN apt-get update
RUN apt-get install -y python3-pip python3-dev python3 python3-pandas


RUN pip3 install --upgrade pip

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip install pymongo
RUN pip install requests
RUN pip install dnspython
RUN pip install timeloop
RUN pip install sodapy

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


CMD python ./main.py



