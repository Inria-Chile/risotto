FROM python:3.8.2-buster

# Install required packages
RUN apt-get update && \
  apt-get install -y \
  python-dev \
  rm -rf /var/lib/apt/lists/*

# Set workdir and install python requirements
WORKDIR /usr/src/risotto
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run prerelease script
RUN python scripts/prerelease.py

# Expose port
EXPOSE 8000

# Run development server in runtime
CMD ["voila --port=8000 --no-browser --enable_nbextensions=True 06_GUI.ipynb"]