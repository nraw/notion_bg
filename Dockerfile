FROM python:3.8-buster

RUN mkdir /home/app && useradd app && chown app:app /home/app

# fix encoding issues
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
# making stdout unbuffered (any non empty string works)
ENV PYTHONUNBUFFERED="thisistheway"
ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update \
    && apt-get install -y \
    git \
    jq \
    vim \
    tree \
    && rm -rf /var/lib/apt/lists/*

RUN pip install ipython

# install python specific packages
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . app
WORKDIR app
