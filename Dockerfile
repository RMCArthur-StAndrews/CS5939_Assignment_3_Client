FROM python:slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1

# Install required Python packages
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the PYTHONPATH to the project's root directory
ENV PYTHONPATH=/app

ENV CLOUD_PATH=10.0.0.2

# Expose the port the app runs on (Keep on 4000 as other services run elsewhere)
EXPOSE 4000

# Specify the command to run the application
CMD ["python", "Controllers/Main.py"]