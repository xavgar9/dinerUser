# dinerUser
# Version: 1.0
FROM python:2.7
# Install Python and Package Libraries
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim
# Project Files and Settings
COPY . /opt/www
WORKDIR /opt/www
RUN apt-get update && apt-get install jq vim nano curl -y
RUN pip install -r requirements.txt
# Server
EXPOSE 5000
CMD python2 App.py
