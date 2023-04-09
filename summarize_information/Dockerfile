FROM python:3.11.2 AS builder

RUN apt-get update && \
    apt-get install -y build-essential

RUN pip install uwsgi

FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN apt update && \
    apt install -y vim && \
    apt-get install -y python3-pip && \
    apt install gcc && \
    pip3 install --no-cache-dir -r requirements.txt

COPY . .

COPY --from=builder /usr/local/bin/uwsgi /usr/local/bin/uwsgi

EXPOSE 8000

CMD ["uwsgi", "--ini", "/code/summarize_information.uwsgi.ini"]
