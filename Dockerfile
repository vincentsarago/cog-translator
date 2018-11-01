FROM lambdalinux/baseimage-amzn:2017.03-004

WORKDIR /app

RUN yum update -y && yum upgrade -y
RUN yum install -y python36-devel python36-pip gcc gcc-c++
RUN yum install zip unzip
RUN yum clean all

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

RUN pip-3.6 install pip -U
RUN pip3 install numpy --no-binary numpy

RUN curl -sL https://rpm.nodesource.com/setup_8.x | bash - \
  && yum install -y nodejs

RUN yum install git
RUN npm install git+https://github.com/vincentsarago/ecs-watchbot-fargate.git#master --production
RUN ln -s /app/node_modules/watchbot-fargate/bin/watchbot.js /usr/bin/watchbot

################################################################################
# Install Python dependencies
COPY cog_translator /tmp/app/cog_translator
COPY README.rst /tmp/app/README.rst
COPY setup.py /tmp/app/setup.py

RUN pip3 install /tmp/app/ --no-binary numpy -U
################################################################################
