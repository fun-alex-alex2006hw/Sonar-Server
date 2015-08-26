####################################
#
#  Dockerfile for Sonar Server
#  v0.1 - By Moloch
# 
####################################

FROM python:2.7.10
MAINTAINER moloch

# Install non-pip dependancies
RUN apt-get update -y
RUN apt-get install -y nodejs npm
RUN ln -s /usr/bin/nodejs /usr/bin/node

# Make a directory
RUN mkdir -p /opt/sonar-server

# Copy application into container
ADD . /opt/sonar-server

# Build the jsclient
WORKDIR /opt/sonar-server/jsclient
RUN npm install -g grunt-cli
RUN npm install
RUN grunt

# Install Python dependancies
WORKDIR /opt/sonar-server
RUN pip install -r setup/requirements.txt

# Expose Ports
EXPOSE 80

# Start command
CMD python sonar-server.py --start --logging=INFO

