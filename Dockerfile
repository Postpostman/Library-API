FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
