FROM python:3.10.14-slim
COPY requirements.txt /app/requirements.txt
RUN apt update
RUN apt install libmariadb-dev gcc libc-dev g++ libffi-dev libxml2 unixodbc-dev -y
WORKDIR /app

RUN pip install -r /app/requirements.txt

COPY . /app
CMD ["python", "-u", "main.py"]