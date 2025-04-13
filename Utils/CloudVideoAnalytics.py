import base64
import json
import os
from cryptography.fernet import Fernet
import requests
import traceback

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
        #This is just an example of encryption in the system, beyond a proof of concept use more appropriate tools
        self.cloud_key = base64.urlsafe_b64encode(b"CLOUD_KEY".ljust(32, b'\0'))
        self.edge_key = base64.urlsafe_b64encode(b"EDGE_KEY".ljust(32, b'\0'))
        self.edge_to_cloud_encrypt = Fernet(self.edge_key)
        self.cloud_to_edge_decrypt = Fernet(self.cloud_key)

    def get_analytics(self, encoded_frames: list) -> list:
        """
        Method handles the interaction with the cloud video analytics service.
        :param encoded_frames: The list of frames to be sent to the cloud service for processing
        :return: The data on the images returned from the cloud service, should be in a list of data dictionaries format
        """
        try:

            files = [
                ("image", (f"frame_{i}.bin", self.edge_to_cloud_encrypt.encrypt(frame), "application/octet-stream")) for
                i, frame in enumerate(encoded_frames)]

            response = requests.post(self.base_url + "/stream-handling", files=files)
            response.raise_for_status()

            decrypted_data = self.cloud_to_edge_decrypt.decrypt(response.json()['data'].encode('utf-8'))
            detections = json.loads(decrypted_data)
            return detections
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
        except Exception as e:
            print(f"Error in get_analytics: {e}")
            raise
