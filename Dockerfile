FROM python:slim

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

ENV CLOUD_PATH=http://10.0.0.2:5000

EXPOSE 4000

CMD ["python", "Controllers/Main.py", "--host=0.0.0.0", "--port=4000"]