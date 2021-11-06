FROM python:3.6

WORKDIR /broker2

EXPOSE 6002

COPY requirements.txt /broker2
RUN pip install -r requirements.txt


COPY broker2.py /broker2
CMD python broker2.py


