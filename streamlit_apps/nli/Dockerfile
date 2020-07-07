FROM python:3.8.2-buster

# Install required packages
RUN apt-get update && \
  apt-get install -y \
  python-dev

# Set workdir and install python requirements
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run library build script
RUN python scripts/build.py

EXPOSE 8000