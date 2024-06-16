FROM python:3.10-slim

WORKDIR .
COPY requirements.txt requirements.txt
COPY main.py main.py

RUN pip3 install -r requirements.txt

CMD ["python", "main.py"]