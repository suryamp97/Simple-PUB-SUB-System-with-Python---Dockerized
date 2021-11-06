FROM python:3.6

WORKDIR /subscriber

EXPOSE 5050

COPY requirements.txt /subscriber
RUN pip install -r requirements.txt

COPY templates /subscriber/templates
COPY static /subscriber/static


COPY subscriber.py /subscriber
CMD python subscriber.py


