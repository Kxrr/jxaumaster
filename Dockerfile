FROM index.alauda.cn/library/python:2.7
MAINTAINER Kxrr
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
RUN mkdir /code
COPY . /code
ENV PYTHONPATH /code
WORKDIR /code

RUN sed -i 's/httpredir.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN sed -i '/security.debian.org/d' /etc/apt/sources.list

# RUN apt-get update && apt-get install -y gcc g++ python-software-properties libpq-dev libmysqlclient-dev build-essential python-dev

RUN pip install -r /code/requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

CMD python jxaumaster/app.py
