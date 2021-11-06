FROM python:3.6

WORKDIR /broker3

EXPOSE 6003

COPY requirements.txt /broker3
RUN pip install -r requirements.txt


COPY broker3.py /broker3
CMD python broker3.py


