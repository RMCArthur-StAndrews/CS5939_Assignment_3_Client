
import threading
import os
from dotenv import load_dotenv
from Controllers.ServiceCheck import CloudBackendChecker
from Controllers.FileCheck import FileCheck
from Utils.CloudVideoAnalytics import CloudVideoAnalytics
from Utils.VideoAnalyticsService import VideoAnalyticsService


class Main:
    def __init__(self):
        load_dotenv('edge.env')
        self.api_url = "http://10.0.0.3:5000/utils"
        self.checker = CloudBackendChecker(self.api_url)
        self.checker.start()
        self.video_analytics = VideoAnalyticsService(CloudVideoAnalytics())
        self.file_checker = FileCheck(
            'C:\\Users\\RRHMc\\OneDrive\\Desktop\\CS5939_Assignment_3\\Projects\\Client\\file_check',
            self.video_analytics)
        self.file_checker.start()

    def run(self):
        try:
            while True:
                command = input("Enter 'exit' to stop the application: ")
                if command.lower() == 'exit':
                    break
        finally:
            self.checker.stop()
            self.checker.join()
            self.file_checker.stop()
            self.file_checker.join()
            print("Application has stopped.")

if __name__ == "__main__":
    main_app = Main()
    main_app.run()
