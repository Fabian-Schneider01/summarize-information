FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

WORKDIR /summarize_information

COPY requirements.txt .

RUN pip install -r requirements.txt && \
    apt-get update && \
    apt-get install -y build-essential python-dev python-setuptools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install uwsgi

COPY . .

EXPOSE 8000

CMD ["uwsgi", "--ini", "/summarize_information/summarize_information.uwsgi.ini"]

#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]