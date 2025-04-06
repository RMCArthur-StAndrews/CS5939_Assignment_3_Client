import os
import time
import threading

class FileHandler(threading.Thread):
    """
    Class handles all interactions with the localised file system for retention / processing of videos
    """
    def __init__(self, input_file_path, video_service):
        """
        Constructor for the FileHandler class
        :param input_file_path: Path to the input file
        :param video_service: Determines which video processing service to use
        """
        super().__init__()
        self.input_file_path = input_file_path
        self.processed_folder = input_file_path
        self.output_folder = input_file_path + '\\output'
        self.video_service = video_service
        self.running = True
        self.processed_files = set()

        # Create folders if they don't exist
        os.makedirs(self.input_file_path, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)

    def run(self):
        """
        Method to run the file handler in a separate thread
        :return:
        """
        while self.running:
            self.cleanup_tmp_folder()
            time.sleep(600)  # Pulse every 10 minutes

    def check_for_new_files(self):
        """
        Method handles the inspection of the file area for any new files
        """
        for filename in os.listdir(self.input_file_path):
            if filename.endswith(('.mp4', '.webm')) and filename not in self.processed_files:
                self.processed_files.add(filename)

                input_file = os.path.join(self.input_file_path, filename)
                new_file_name = os.path.splitext(filename)[0] + '_with_detections.mp4'
                output_file = os.path.join(self.output_folder, new_file_name)
                self.process_file(input_file, output_file)

    def process_file(self, input_file, output_file):
        """
        Method handles the processing of a file for video analytics
        :param input_file: The path of the file to be processed
        :param output_file: The new name of the file after processing
        """
        try:
            if not output_file:
                raise ValueError("Output filename is empty")
            self.video_service.run(input_file, output_file)
            processed_file = os.path.join(self.processed_folder, os.path.basename(input_file))
        except ValueError as ve:
            print(f"ValueError processing file {input_file}: {ve}")
        except Exception as e:
            print(f"Error processing file {input_file}: {e}")

    def is_file_in_use(self, file_path):
        """
        Function checks file is actually in use or not
        :param file_path: The file to check
        :return: True if in use, otherwise False
        """
        try:
            os.rename(file_path, file_path)
            return False
        except OSError:
            return True

    def cleanup_tmp_folder(self):
        """
        Method handles the cleanup of the tmp folder of files
        :return:
        """
        tmp_folder = 'tmp'
        if not os.path.exists(tmp_folder):
            os.makedirs(tmp_folder)
        for filename in os.listdir(tmp_folder):
            file_path = os.path.join(tmp_folder, filename)
            if not self.is_file_in_use(file_path):
                try:
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")
                except Exception as e:
                    print(f"Error removing file {file_path}: {e}")

    def stop(self):
        """
        Method stops the thread when called
        """
        self.running = False
