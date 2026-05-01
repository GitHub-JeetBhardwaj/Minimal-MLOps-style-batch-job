FROM python:3.9-slim

RUN useradd -m -s /bin/bash appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py .
COPY config.yaml .
COPY data.csv .

RUN chown -R appuser:appuser /app
USER appuser

CMD ["python", "run.py", "--input", "data.csv", "--config", "config.yaml", "--output", "metrics.json", "--log-file", "run.log"]