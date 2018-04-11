#!/usr/bin/env python3

import cv2
import numpy as np

import time
import datetime

cap = cv2.VideoCapture(0)


def main():
    cv2.namedWindow('feedback')
    cv2.moveWindow('feedback', 600, 600)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    center = (int(width / 2), int(height / 2))
    markerrad = int(height / 4)

    print(width)
    print(height)

    def updateBrightness(val):
        nonlocal brightness
        brightness = val

    cv2.createTrackbar("brightness", 'feedback', 0, 255, updateBrightness)
    cv2.setTrackbarMin('brightness', 'feedback', -255)

    downsample = False
    guide = True
    brightness = 50
    trailing_average_weights = []  # Last element is weight to give previous frame, etc...
    old_frames = []

    while True:
        ret, frame = cap.read()

        if downsample:
            # TODO: this

            pass

        if guide:
            # TODO: Clean up crosshair generation
            cv2.circle(frame, center, markerrad, (255, 0, 0), 2)
            cv2.drawMarker(frame, (center[0] + markerrad, center[1]), (0, 0, 255), cv2.MARKER_CROSS, 20, 2, cv2.FILLED)
            cv2.drawMarker(frame, (center[0] - markerrad, center[1]), (0, 0, 255), cv2.MARKER_CROSS, 20, 2, cv2.FILLED)
            cv2.drawMarker(frame, (center[0], center[1] + markerrad), (0, 0, 255), cv2.MARKER_CROSS, 20, 2, cv2.FILLED)
            cv2.drawMarker(frame, (center[0], center[1] - markerrad), (0, 0, 255), cv2.MARKER_CROSS, 20, 2, cv2.FILLED)
            pass

        if brightness != 0:
            bright = np.full_like(frame, abs(brightness))

            if brightness > 0:
                cv2.add(frame, bright, frame)
            else:
                cv2.subtract(frame, bright, frame)

        if trailing_average_weights:
            old_frames.append(np.copy(frame))
            if len(old_frames) >= len(trailing_average_weights):
                old_frames = old_frames[-len(trailing_average_weights):]
                frame = frame * (1.0 - sum(trailing_average_weights))
                for w, f in zip(trailing_average_weights, old_frames):
                    frame = frame + f * w
                frame = np.array(frame, dtype=np.uint8)

        key = chr(cv2.waitKey(1) & 0xFF)
        if key == 'q':
            # Quit if the "q" key is pressed over the window
            break
        if key == 's':
            # TODO:  Save in image directory to be gitignored
            savename = datetime.datetime.now().strftime("%Y-%M-%d-%H:%M")
            savename += '.png'
            print(savename)
            cv2.imwrite(savename,frame)
        if key == 'd':
            downsample = not downsample
        if key == 'g':
            guide = not guide
        if key == 'a':
            if trailing_average_weights:
                trailing_average_weights = []
                print("Trailing Averaging Disabled")
            else:
                trailing_average_weights = [.5,0]
                print("Trailing Averaging enabled: ", trailing_average_weights)

        cv2.imshow('feedback', frame)


if __name__ == '__main__':
    main()
