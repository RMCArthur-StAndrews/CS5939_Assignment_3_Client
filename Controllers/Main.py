import logging
import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from Utils.CloudVideoAnalytics import CloudVideoAnalytics
from Utils.VideoAnalyticsService import VideoAnalyticsService
import mimetypes
import os

"""
Load Environment Variables for the session if present
"""
dotenv_path = find_dotenv('edge.env')
if not dotenv_path:
    raise EnvironmentError("edge.env file not found")
load_dotenv(dotenv_path)

"""
Flask Configuration
"""
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)  # Enable CORS

# Ensure the CLOUD_PATH environment variable is set
base_url = os.getenv('CLOUD_PATH')
if not base_url:
    raise EnvironmentError("CLOUD_PATH environment variable is not set")

@app.route('/check-signal', methods=['GET'])
def check_signal():
    """
    Check the connection to the Cloud API by sending a GET request to the /utils endpoint
    (generic calling which will return 200 if the service is running)
    :return: 200 if successful, 500 if failed
    """
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
    """
    Send video file to cloud for processing
    :return:
    """
    try:
        file = request.files['file']
        input_file_path = os.path.join('tmp', file.filename)
        os.makedirs(os.path.dirname(input_file_path), exist_ok=True)
        file.save(input_file_path)
        output_file_name = "output_" + file.filename
        service = VideoAnalyticsService(CloudVideoAnalytics())
        output_file_path = service.run(input_file_path, output_file_name)
        logging.info("Output file path: " + output_file_path)
        mimetype, _ = mimetypes.guess_type(output_file_path)
        file_size = os.path.getsize(output_file_path)
        logging.info("File size: " + str(file_size))
        response = send_file(output_file_path, as_attachment=True, download_name=output_file_name, mimetype=mimetype, conditional=True)
        response.headers['Content-Length'] = file_size
        return response, 200
    except Exception as e:
        return jsonify(f"Error processing video: {e}"), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)