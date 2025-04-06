import os
import random
import cv2

class VideoAnalyticsService:
    """
    Class to handle video analytics using a provided model service.
    """
    def __init__(self, model_service):
        """
        Constructor for the VideoAnalyticsService class.
        :param model_service: The service used for video analytics (Local, Edge Server, Cloud)
        """
        self.model_service = model_service
        self.color_map = {}
        self.thickness = 2

    def run(self, input_path, output_file_name):
        """
        Method to run the video analytics on the input video file.
        :param input_path: The file path for the video to process
        :param output_file_name: The name (and path) of the to be created output file
        :return: The absolute path of the output file
        """
        cap = self.load_video(input_path)
        filename = os.path.basename(input_path)
        frame_width, frame_height, fps = self.get_video_properties(cap)
        out, file_path = self.create_video_writer(output_file_name, frame_width, frame_height, fps)
        if not cap.isOpened():
            raise ValueError("Failed to open prior to load")
        try:
            self.process_video_frames(cap, out, self.model_service)
        finally:
            self.release_resources(cap, out)

        return file_path

    def load_video(self, file_path):
        """
        Method to load the video file for processing.
        :param file_path: The file path to open
        :return: The loaded video file if available, otherwise an error
        """
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            raise ValueError("Failed to open video file")
        return cap

    def get_video_properties(self, cap):
        """
        Method to get the metadata of the video file.
        :param cap: The video file to retrieve the metadata from
        :return: The metadata of the video file (frame width, frame height, fps)
        """
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        return frame_width, frame_height, fps

    def create_video_writer(self, file_name, frame_width, frame_height, fps):
        """
        Method to create the video writer for the output file.
        :param file_name: The new file name
        :param frame_width: The width of the video
        :param frame_height: The height of the video
        :param fps: The frames per second of the video
        :return: The newly created output file and its absolute path
        """
        output_file_path = os.path.join('tmp', file_name)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        video_writer = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc(*'VP80'), fps,
                                       (frame_width, frame_height))
        return video_writer, os.path.abspath(output_file_path)

    def process_video_frames(self, cap, out, model_service):
        """
        Main method for processing frames of the video file.
        :param cap: The video file to process
        :param out: The name of the output file
        :param model_service: The video service to use
        """
        frame_skip = 6  # Number of frames to skip
        frame_count = 0
        last_result = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % frame_skip == 0:
                frame_bytes = self.encode_frame_to_bytes(frame)
                last_result = model_service.get_analytics(frame_bytes)
                self.validate_result(last_result)

            if last_result:
                self.draw_detections(frame, last_result['detections'])
            out.write(frame)

    def encode_frame_to_bytes(self, frame):
        """
        Method to encode a video frame to bytes.
        :param frame: The video frame to encode
        :return: The encoded frame as bytes
        """
        _, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

    def validate_result(self, result):
        """
        Method to validate the result from the model service.
        :param result: The result to validate
        :raises ValueError: If the result format is invalid
        """
        if 'detections' not in result or not isinstance(result['detections'], list):
            raise ValueError("Invalid result format")

    def release_resources(self, *resources):
        """
        Method to release resources such as video capture and writer.
        :param resources: The resources to release
        """
        for resource in resources:
            resource.release()

    def play_video(self, file_path):
        """
        Method to play the video file.
        :param file_path: The file path of the video to play
        """
        cap = cv2.VideoCapture(file_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Output Video with Detections', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def draw_single_detection(self, frame, detection):
        """
        Method to draw a single detection box on the frame.
        :param frame: The frame to place the detection on
        :param detection: The single instance of the detection to draw (as a boundary box)
        :return: The updated frame
        """
        boundary = detection['bbox'][0]
        classifier_id = detection['class']
        classifier_name = detection['name']
        assurance_score = detection['confidence']

        if classifier_id not in self.color_map:
            self.color_map[classifier_id] = self.generate_random_color()

        cv2.rectangle(frame, (int(boundary[0]), int(boundary[1])), (int(boundary[2]), int(boundary[3])),
                      self.color_map[classifier_id], self.thickness)
        label = f"Class: {classifier_name}, Conf: {assurance_score:.2f}"
        cv2.putText(frame, label, (int(boundary[0]), int(boundary[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    self.color_map[classifier_id], self.thickness)
        return frame

    def draw_detections(self, frame, detections):
        """
        Method to draw multiple detection boxes on the frame.
        :param frame: The frame to place the detections on
        :param detections: The list of detections to draw
        :return: The updated frame
        """
        for detection in detections:
            frame = self.draw_single_detection(frame, detection)
        return frame

    def generate_random_color(self):
        """
        Method to generate a random color.
        :return: A tuple representing a random color (B, G, R)
        """
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
