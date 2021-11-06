FROM python:3.6

WORKDIR /broker1

EXPOSE 6001

COPY requirements.txt /broker1
RUN pip install -r requirements.txt


COPY broker1.py /broker1
CMD python broker1.py


