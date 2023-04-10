from python:3.9.6-buster
RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y

WORKDIR /easy_flat
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade -r requirements.txt
ENV HOME=/home/app
ENV APP_HOME=/home/easy_flat/
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh
COPY . .
