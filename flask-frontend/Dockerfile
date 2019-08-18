FROM ubuntu:18.10

# Install Python3
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx
RUN pip3 install uwsgi

# Define work directory
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

# Install requirement
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "run.py" ]