FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Copy the workflow code
COPY . .

# Install Temporal Python SDK and dependencies
RUN pip install -r requirements.txt

# Keep container running for development
# CMD ["tail", "-f", "/dev/null"]
# CMD ["python", "-u", "worker.py"] 