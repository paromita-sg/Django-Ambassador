FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Install MySQL client
RUN apt-get update && apt-get install -y default-mysql-client && \
    pip install -r requirements.txt

COPY . /app

CMD python manage.py wait_for_db && python manage.py runserver 0.0.0.0:8000