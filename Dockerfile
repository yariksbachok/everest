FROM python:3.8

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
