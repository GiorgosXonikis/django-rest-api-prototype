# Pull base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
#COPY Pipfile Pipfile.lock /code/
#RUN pip install pipenv && pipenv install --system
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy project
COPY . /app/