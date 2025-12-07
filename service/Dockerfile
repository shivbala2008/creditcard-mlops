FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Optional: make sure Python can import from /app
ENV PYTHONPATH=/app

# Expose API port
EXPOSE 8000

# Start the FastAPI app (package mode)
CMD ["uvicorn", "service.app:app", "--host", "0.0.0.0", "--port", "8000"]
