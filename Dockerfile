FROM python:slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Load environment variables from edge.env file
COPY edge.env .
RUN set -o allexport && \
    source edge.env && \
    set +o allexport

# Set the PYTHONPATH to the project's root directory
ENV PYTHONPATH=/app

# Specify the command to run the application
CMD ["python", "Controllers/Main.py"]