FROM joyzoursky/python-chromedriver:3.7-alpine3.8-selenium
RUN pip install bs4 xlsxwriter
WORKDIR /workdir
ADD . .
CMD sh