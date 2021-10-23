FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY templates /app/templates
COPY static /app/static


COPY app.py /app
CMD python app.py


