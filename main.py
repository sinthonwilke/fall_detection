from poseDetectModule import poseDetect
from fallCalculation import fallCalculation
from callHelp import callHelp

import cv2
import time


class VideoProcessor:
    def __init__(self, video_name):
        self.video_path = (f'videoRef/{video_name}')
        self.key_delay = 0.06  # Adjust this value to set the key input delay

        self.cap = cv2.VideoCapture(self.video_path)
        self.pose_detector = poseDetect()
        self.fall_calculator = fallCalculation()
        self.callHelp = callHelp()

        self.pTime = 0
        self.total_fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        self.last_key_time = time.time()

        self.color = {
            'green': (0, 255, 0),
            'yellow': (0, 255, 255),
            'orange': (0, 165, 255),
            'red': (0, 0, 255),
        }

    def process_frame(self, frame):
        cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime
        self.total_fps += fps
        self.frame_count += 1
        avg_fps = self.total_fps / self.frame_count
        elapsed_time = time.time() - self.start_time
        total_time_formatted = time.strftime('%H:%M:%S', time.gmtime(elapsed_time)) + f'.{int((elapsed_time % 1) * 100)}'

        cv2.putText(frame, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, self.color['green'], 2)
        cv2.putText(frame, f'FPS(avg): {int(avg_fps)}', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, self.color['green'], 2)
        cv2.putText(frame, f'Time Played: {total_time_formatted}', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.75, self.color['green'], 2)

        cv2.imshow('Pose Estimation', frame)

    def handle_key_input(self, key):
        current_time = time.time()
        if current_time - self.last_key_time < self.key_delay:
            return  # Skip handling the key if the delay hasn't passed

        if key == 32:  # Check for the space bar key
            self.last_key_time = current_time
            self.pause_video()
        elif key == ord(','):  # Comma key
            self.last_key_time = current_time
            self.adjust_position(-10)
        elif key == ord('.'):  # Period key
            self.last_key_time = current_time
            self.adjust_position(5)
        elif key == 27:  # Check for the 'esc' key
            self.last_key_time = current_time
            self.release_resources()

    def pause_video(self):
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # Break the loop on space bar key
                break
            elif key == 27:  # Release resources and close windows on 'esc' key
                self.release_resources()
                return

    def adjust_position(self, frames):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cap.get(cv2.CAP_PROP_POS_FRAMES) + frames)

    def release_resources(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def where_magic_happens(self, frame):
        if self.pose_detector.detect(frame):
            self.fall_calculator.setValue(self.pose_detector.get_needed_landmarks())

            if self.fall_calculator.pose1():
                self.pose_detector.draw_bbox('standing', self.color['green'])
                self.fall_calculator.setLastStandToFall_time(self.fall_calculator.getStandToFall_time())
                self.fall_calculator.resetFall_time()
                self.callHelp.resetCall()
                self.fall_calculator.setTotalStandToFall_status(True)
            else:
                if self.fall_calculator.pose0():
                    fallTime = self.fall_calculator.getFall_time()

                    if self.fall_calculator.getTotalStandToFall_status():
                        self.fall_calculator.setTotalStandToFall_status(False)
                        self.fall_calculator.setTotalStandToFall_time()

                    if self.fall_calculator.getTotalStandToFall_time() < 1:
                        self.pose_detector.draw_bbox(f'Fall ({fallTime:.2f} s)', self.color['red'])
                        if fallTime > 5 and not self.callHelp.isCall():
                            self.callHelp.call()
                    else:
                        self.pose_detector.draw_bbox('Laying', self.color['orange'])
                else:
                    self.pose_detector.draw_bbox('Falling', self.color['yellow'])
                    self.fall_calculator.resetFall_time()
                    self.callHelp.resetCall()
                    self.fall_calculator.setTotalStandToFall_status(True)

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            self.where_magic_happens(frame)
            self.process_frame(frame)

            key = cv2.waitKey(1) & 0xFF
            self.handle_key_input(key)


if __name__ == '__main__':
    video_name = 'fall2.mov'
    video_processor = VideoProcessor(video_name)
    video_processor.run()
