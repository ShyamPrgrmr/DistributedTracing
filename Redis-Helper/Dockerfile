FROM bitnami/python:latest
USER root

COPY . .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN touch application.log
WORKDIR /app/src
CMD ["python", "main.py"]