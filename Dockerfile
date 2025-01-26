# Dockerfile
FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code BEFORE running Django commands
COPY . .

# Run migrations
RUN cd sqlscope && python manage.py makemigrations && python manage.py migrate

RUN cd sqlscope ;DJANGO_SUPERUSER_PASSWORD=changeme python manage.py createsuperuser --noinput --username admin --email sqlscope@example.com

# Expose port
EXPOSE 8000

# Command to start the application
CMD ["python", "sqlscope/manage.py", "runserver", "0.0.0.0:8000"]
