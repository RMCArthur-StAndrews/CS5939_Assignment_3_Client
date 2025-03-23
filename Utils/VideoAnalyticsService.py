import os
import random

import cv2


class VideoAnalyticsService:
    def __init__(self, model_service):
        self.model_service = model_service
        self.color_map = {}
        self.thickness = 2

    def run(self, input_path, output_file_name):
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
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            raise ValueError("Failed to open video file")
        return cap

    def get_video_properties(self, cap):
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        return frame_width, frame_height, fps

    def create_video_writer(self, file_name, frame_width, frame_height, fps):
        output_file_path = os.path.join('tmp', file_name)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        video_writer = cv2.VideoWriter(output_file_path, cv2.VideoWriter_fourcc(*'VP80'), fps,
                                       (frame_width, frame_height))
        return video_writer, os.path.abspath(output_file_path)

    def process_video_frames(self, cap, out, model_service):
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
        _, buffer = cv2.imencode('.jpg', frame)
        return buffer.tobytes()

    def validate_result(self, result):
        if 'detections' not in result or not isinstance(result['detections'], list):
            raise ValueError("Invalid result format")

    def release_resources(self, *resources):
        for resource in resources:
            resource.release()

    def play_video(self, file_path):
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
        for detection in detections:
            frame = self.draw_single_detection(frame, detection)
        return frame

    def generate_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
