# Dockerfile
# Use the official Python image as a base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app/

# Ensure port 8000 is available to the world outside this container
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]