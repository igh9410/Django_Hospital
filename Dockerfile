# Stage 1: Build
FROM python:3.10 as build-stage

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock (if available)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy the entire application
COPY . /app/

# Test Phase
RUN poetry run python manage.py test

# Stage 2: Runtime
FROM python:3.10-slim as build-release-stage

WORKDIR /app

# Copy installed dependencies from the build stage
COPY --from=build-stage /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=build-stage /usr/local/bin /usr/local/bin
COPY --from=build-stage /app /app

EXPOSE 8000

# Add and run as non-root user
RUN useradd -m myuser
USER myuser

# Command to run the application
CMD ["gunicorn", "django_hospital.wsgi:application", "--bind", "0.0.0.0:8000"]
