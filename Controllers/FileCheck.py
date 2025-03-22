import os
import time
import threading
import shutil
from Utils.VideoAnalyticsService import VideoAnalyticsService

class FileCheck(threading.Thread):
    def __init__(self, input_file_path, video_service):
        super().__init__()
        self.input_file_path = input_file_path
        self.processed_folder = input_file_path+'\\processed'
        self.output_folder = input_file_path+'\\output'
        self.video_service = video_service
        self.running = True
        self.processed_files = set()

        # Create folders if they don't exist
        os.makedirs(self.input_file_path, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)

    def run(self):
        while self.running:
            self.check_for_new_files()
            time.sleep(30)  # Pulse every 5 seconds

    def check_for_new_files(self):
        for filename in os.listdir(self.input_file_path):
            if filename.endswith(('.mp4', '.webm')) and filename not in self.processed_files:
                self.processed_files.add(filename)

                input_file = os.path.join(self.input_file_path, filename)
                new_file_name = os.path.splitext(filename)[0] + '_with_detections.mp4'
                output_file = os.path.join(self.output_folder, new_file_name)
                self.process_file(input_file, output_file)

    def process_file(self, input_file, output_file):
        try:
            if not output_file:
                raise ValueError("Output filename is empty")
            self.video_service.run(input_file, output_file)
            processed_file = os.path.join(self.processed_folder, os.path.basename(input_file))
            shutil.move(input_file, processed_file)
        except ValueError as ve:
            print(f"ValueError processing file {input_file}: {ve}")
        except Exception as e:
            print(f"Error processing file {input_file}: {e}")

    def stop(self):
        self.running = False