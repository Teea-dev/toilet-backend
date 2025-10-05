FROM python:3.13.0-slim-bookworm

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PORT=5000

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential \
    postgresql-client \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .


RUN pip install --no cache-dir -r requirements.txt


COPY . .


RUN mkdir -p /app/instance

EXPOSE 5000


HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD python -c "import requests; requests.get ("http://localhost:5000/")"

CMD ["gunicorn", "--bind", "0.0.0:5000", "--workers", "2", "--timeout", "120","app:app"]