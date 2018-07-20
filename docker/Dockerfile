FROM python:3.6

ADD ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir /app

ADD ./app/ /app/app/
ADD ./*.py /app/

WORKDIR /app