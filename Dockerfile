FROM python:3.7

RUN apt-get update && apt-get install -y git libnss3-dev chromium=76.0.3809.100-1~deb10u1

# install chromedriver
ADD chromedriver /usr/bin/
RUN pip install selenium==3.14.1
RUN pip install bs4 xlsxwriter click
WORKDIR /workdir
ADD . .
CMD sh
