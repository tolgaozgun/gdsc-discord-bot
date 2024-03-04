# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10-alpine

RUN apk update
RUN apk add chromium
RUN apk add chromium-chromedriver

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# After copying your project files
COPY . /usr/src/app/

WORKDIR /usr/src/app

CMD ["python", "main.py"]
