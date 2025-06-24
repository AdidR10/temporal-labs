FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Install Temporal Python SDK
# RUN pip install temporalio

# Copy the workflow code
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Keep container running for development
CMD ["python", "worker.py"] 