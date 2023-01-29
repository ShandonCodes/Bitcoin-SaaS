
FROM python:3.10-alpine

COPY server.py app.py
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["flask", "run" ,"--host=0.0.0.0"]