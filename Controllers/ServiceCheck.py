import threading
import time
import requests
import os

class CloudBackendChecker(threading.Thread):
    def __init__(self, api_url):
        super().__init__()
        self.api_url = api_url
        self.running = True

    def run(self):
        while self.running:
            try:
                response = requests.get(self.api_url)
                rd = response.json()
                if rd['error'] == 200:
                    print("Cloud backend is running")
                    os.environ["LOCAL_MODE"] = "False"
                else:
                    print("Cloud backend is not running")
                    os.environ["LOCAL_MODE"] = "True"
            except Exception as e:
                print(f"Error checking cloud backend: {e}")
                os.environ["LOCAL_MODE"] = "True"
            time.sleep(5)

    def stop(self):
        self.running = False