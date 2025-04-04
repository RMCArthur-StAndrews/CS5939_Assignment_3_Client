import base64
import json
import os
from cryptography.fernet import Fernet
import requests

class CloudVideoAnalytics:
    """
    Class handles the interaction with the cloud video analytics service.
    """
    def __init__(self):
        """
         Constructor for cloud analytics class

        :return:
        """
        self.base_url = os.environ['CLOUD_PATH']
        if not self.base_url:
            raise ValueError("CLOUD_PATH environment variable is not set.")
        # Here demonstrates the use of the end to end encryption as an example
        self.cloud_key = base64.urlsafe_b64encode(b"CLOUD_KEY".ljust(32, b'\0'))
        self.edge_key = base64.urlsafe_b64encode(b"EDGE_KEY".ljust(32, b'\0'))
        self.edge_to_cloud_encrypt = Fernet(self.edge_key)
        self.cloud_to_edge_decrypt = Fernet(self.cloud_key)

    def get_analytics(self, encoded_frame: bytes) -> dict:
        """
        Method handles the interaction with the cloud video analytics service.
        :param encoded_frame: The frame to be sent to the cloud service for processing
        :return: The data on the image returned from the cloud service, should be in data dictionary format
        """
        try:
            encrypted_frame = self.edge_to_cloud_encrypt.encrypt(encoded_frame)
            response = requests.post(self.base_url + "/stream-handling", files={"image": encrypted_frame})
            response.raise_for_status()
            decrypt = self.cloud_to_edge_decrypt.decrypt(response.json()['data'].encode())
            detections = json.loads(decrypt)
            return detections
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
        except Exception as e:
            print(f"Error in get_analytics: {e}")
            raise
