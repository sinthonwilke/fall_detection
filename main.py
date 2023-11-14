import cv2
from poseDetectModule import poseDetect


def main():
    cap = cv2.VideoCapture('videoRef/1.mp4')
    # cap = cv2.VideoCapture(1)

    poseDetector = poseDetect()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if poseDetector.detect(frame):
            poseDetector.draw_landmarks()

        cv2.imshow('Pose Estimation', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
