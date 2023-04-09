FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN apt update && \
    apt install -y vim && \
    apt-get install -y python3-pip && \
    apt install gcc && \
    pip3 install uwsgi 

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uwsgi", "--ini", "/code/summarize_information.uwsgi.ini"]
