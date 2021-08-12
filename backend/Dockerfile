FROM ubuntu:20.04
LABEL maintainer="mtlv"

COPY . /home/store_resource_management
RUN apt-get update \
      && apt-get upgrade -yq \
      && apt-get install -yq apt-utils \
                             python3.6 \
                             python3-pip \
                             git \
                             libmysqlclient-dev
RUN pip3 install --upgrade pip setuptools wheel
# RUN pip3 install Django==2.2.6
RUN pip3 install django
RUN pip3 install djangorestframework
# RUN pip3 install mysqlclient==1.4.4
RUN pip3 install mysqlclient
# RUN pip3 install paramiko==2.7.2


# utf-8
RUN apt-get install locales -y
RUN locale-gen zh_CN.UTF-8
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8

CMD python3 manage.py runserver