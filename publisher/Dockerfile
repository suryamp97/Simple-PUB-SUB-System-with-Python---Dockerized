FROM python:3.6

WORKDIR /publisher

EXPOSE 5000

COPY requirements.txt /publisher
RUN pip install -r requirements.txt

COPY templates /publisher/templates
COPY static /publisher/static


COPY publisher.py /publisher
CMD python publisher.py


