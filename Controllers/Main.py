import logging
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from Controllers.ServiceCheck import CloudBackendChecker
from Utils.CloudVideoAnalytics import CloudVideoAnalytics
from Utils.VideoAnalyticsService import VideoAnalyticsService
import threading
import mimetypes
import os

# Load environment variables from a .env file
dotenv_path = find_dotenv('edge.env')
if not dotenv_path:
    raise EnvironmentError("edge.env file not found")
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)  # Enable CORS

# Ensure the CLOUD_PATH environment variable is set
base_url = os.getenv('CLOUD_PATH')
if not base_url:
    raise EnvironmentError("CLOUD_PATH environment variable is not set")

@app.route('/check-signal', methods=['GET'])
def check_signal():
    try:
        response = requests.get(base_url + "/utils")
        if response.status_code== 200:
            return jsonify("Connection Successful"), 200
        else:
            return jsonify("Connection Failed"), 500
    except Exception as e:
        return jsonify(f"Error checking signal: {e}"), 500


@app.route('/process-video', methods=['POST'])
def process_video():
    file = request.files['file']
    input_file_path = os.path.join('tmp', file.filename)

    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(input_file_path), exist_ok=True)

    file.save(input_file_path)
    output_file_name = "output_" + file.filename
    service = VideoAnalyticsService(CloudVideoAnalytics())
    output_file_path = service.run(input_file_path, output_file_name)
    logging.info("Output file path: " + output_file_path)
    # Detect the mimetype dynamically
    mimetype, _ = mimetypes.guess_type(output_file_path)

    # Get the file size
    file_size = os.path.getsize(output_file_path)
    logging.info("File size: " + str(file_size))
    # Return the processed file in the response with correct headers
    response = send_file(output_file_path, as_attachment=True, download_name=output_file_name, mimetype=mimetype, conditional=True)
    response.headers['Content-Length'] = file_size
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)