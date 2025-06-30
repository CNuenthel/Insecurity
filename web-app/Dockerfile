# Use a slim Python base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt .
COPY insecure_app.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create uploads directory
RUN mkdir /app/uploads

# Expose the Flask port
EXPOSE 5050

# Run the app
CMD ["python", "insecure_app.py"]
