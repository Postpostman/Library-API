FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
