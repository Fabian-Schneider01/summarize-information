FROM python:3.11.2

ENV PYTHONUNBUFFERED=1

WORKDIR /summarize_information

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8000

CMD ["uwsgi", "--ini", "/code/summarize_information.uwsgi.ini"]

#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]