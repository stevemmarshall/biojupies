FROM ubuntu:17.10

MAINTAINER Denis Torre <denis.torre@mssm.com>

RUN apt-get update && apt-get install -y python3
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get update && apt-get install -y python3-dev
RUN apt-get update && apt-get install -y libmysqlclient-dev

RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install Flask
RUN pip3 install sqlalchemy
RUN pip3 install flask-sqlalchemy
RUN pip3 install pymysql
RUN pip3 install google-cloud
RUN pip3 install h5py

RUN apt-get update && apt-get install -y python3-setuptools
RUN apt-get update && apt-get install -y nginx uwsgi-core
RUN apt-get update && apt-get install -y libpcre3 libpcre3-dev
RUN pip3 install uwsgi
RUN pip3 install xlrd
RUN pip3 install sentry-sdk[flask]==0.3.5
RUN pip3 install bs4
RUN pip3 install lxml

RUN mkdir biojupies
COPY . /biojupies
WORKDIR /biojupies
RUN chmod +x boot.sh; chmod -R 777 /biojupies/app/static;

ENTRYPOINT mkdir -p .config/gcloud; echo $APPLICATION_DEFAULT_CREDENTIALS > $GOOGLE_APPLICATION_CREDENTIALS; ./boot.sh