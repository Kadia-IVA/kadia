FROM python:3.7-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py /app/
CMD cd /app && uvicorn run:app --port $PORT --host 0.0.0.0
