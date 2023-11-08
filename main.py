import cv2
from pyparsing import col
from poseDetectModule import poseDetect


def main():
    cap = cv2.VideoCapture('videoRef/1.mp4')
    poseDetector = poseDetect()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        poseDetector.detect(frame)
        poseDetector.draw_bbox(frame, text='Detected', margin=100)

        cv2.imshow('Pose Estimation', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
