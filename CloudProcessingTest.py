import os
import unittest
from Utils.CloudVideoAnalytics import CloudVideoAnalytics
from Utils.VideoAnalyticsService import VideoAnalyticsService

class TestVideoAnalyticsService(unittest.TestCase):

    def setUp(self):
        # Set up the environment variable for the cloud path
        os.environ["CLOUD_PATH"] = "http://127.0.0.1:5000"
        os.environ["CLOUD_KEY"] = "CLOUD_KEY"
        os.environ["EDGE_KEY"] = "EDGE_KEY"

        self.model_service = CloudVideoAnalytics()

        self.video_service = VideoAnalyticsService(self.model_service)

    def test_process_video(self):
        input_path = "test.webm"
        output_path = "output_test.mp4"

        result_path = self.video_service.run(input_path, output_path)

        self.assertTrue(os.path.exists(result_path))

if __name__ == "__main__":
    unittest.main()