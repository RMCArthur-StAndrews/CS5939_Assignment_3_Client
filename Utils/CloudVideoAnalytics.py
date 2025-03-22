
import base64
import json
import os
from cryptography.fernet import Fernet
import requests

class CloudVideoAnalytics:

    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        if not self.base_url:
            raise ValueError("CLOUD_PATH environment variable is not set.")
        self.cloud_key = base64.urlsafe_b64encode(b"CLOUD_KEY".ljust(32, b'\0'))
        self.edge_key = base64.urlsafe_b64encode(b"EDGE_KEY".ljust(32, b'\0'))
        self.edge_to_cloud_encrypt = Fernet(self.edge_key)
        self.cloud_to_edge_decrypt = Fernet(self.cloud_key)

    def get_analytics(self, encoded_frame: bytes) -> dict:
        encrypted_frame = self.edge_to_cloud_encrypt.encrypt(encoded_frame)
        response = requests.post(self.base_url + "/stream-handling", files={"image": encrypted_frame})
        decrypt = self.cloud_to_edge_decrypt.decrypt(response.json()['data'].encode())
        detections = json.loads(decrypt)
        return detections