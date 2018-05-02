#!/usr/bin/env python3
import datetime
import os
import time
from typing import Optional

import cv2
import numpy as np

cap = cv2.VideoCapture(1)

xvid = cv2.VideoWriter_fourcc(*'XVID')


def main():
    # Setup controls window
    cv2.namedWindow('controls')
    cv2.imshow('controls', np.zeros([1, 800]))

    # Set up image window
    cv2.namedWindow('feedback')
    windowx = 600
    windowy = 200
    cv2.moveWindow('feedback', windowx, windowy)
    ret, frame = cap.read()

    cv2.imshow('feedback', frame)
    time.sleep(0.5)  # pause 0.5 seconds

    videocap = None  # type: Optional[cv2.VideoWriter]

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    center = (int(width / 2), int(height / 2))
    markerrad = int(height / 4)

    print(width)
    print(height)

    def updateBrightness(val):
        nonlocal brightness
        brightness = val

    # Set up trackbars
    cv2.createTrackbar('brightness', 'controls', 0, 255, updateBrightness)
    # cv2.createTrackbar('compensation', 'controls', 0, 200, None)
    cv2.setTrackbarPos('compensation','controls', 100)
    cv2.setTrackbarMin('brightness', 'controls', -255)

    overlay_idx = 0
    overlay_frame = None

    # Set up overlay images
    def increment_overlay(delta):
        overlay_names = os.listdir('overlays')
        overlay_names.sort()
        nonlocal overlay_idx, overlay_frame

        overlay_idx += delta
        overlay_idx %= len(overlay_names)

        overlay_frame = cv2.imread('overlays/'+overlay_names[overlay_idx])
        overlay_frame = cv2.resize(overlay_frame, dsize=(int(width), int(height)))
        print('Displaying overlay frame "{}"'.format(overlay_names[overlay_idx]))

    increment_overlay(0)

    compensation = cv2.imread("transfer-func-blurred.png")
    compensation = cv2.resize(compensation, dsize=(int(width), int(height)))
    compensation = np.array(compensation, dtype=np.float32) / 256.0
    compensation = (np.negative(compensation) + 1) + np.min(compensation)

    # print(compensation[100,100:200])

    # Set up flags
    compensate = False  # Compensate for screen brightness bloom
    downsample = False
    guide = True
    brightness = 0
    trailing_average_weights = []  # Last element is weight to give previous frame, etc...
    old_frames = []
    overlay = False

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

        if compensate:
            frame = np.array(frame, dtype=np.float32)

            frame = frame * compensation

            frame = np.array(frame, dtype=np.uint8)

        if trailing_average_weights:
            old_frames.append(np.copy(frame))
            if len(old_frames) >= len(trailing_average_weights):
                old_frames = old_frames[-len(trailing_average_weights):]
                frame = frame * (1.0 - sum(trailing_average_weights))
                for w, f in zip(trailing_average_weights, old_frames):
                    frame = frame + f * w
                frame = np.array(frame, dtype=np.uint8)

        if overlay:
            frame = overlay_frame

        if videocap:
            videocap.write(frame)

        key = chr(cv2.waitKey(1) & 0xFF)
        if key == 'q':
            # Quit if the "q" key is pressed over the window
            break
        if key == 'x':
            savename = 'photos/' + datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            savename += '.png'
            print(savename)
            cv2.imwrite(savename, frame)

        if key == 'z':
            # Toggle video recording
            if videocap:
                print("Stopping recording")
                videocap.release()
                videocap = None
            else:
                savename = 'videos/' + datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
                savename += '.avi'
                print("Starting recording: " + savename)
                videocap = cv2.VideoWriter(savename, xvid, 30.0, (width, height))

        if key == 'r':
            downsample = not downsample
        if key == 'g':
            guide = not guide
        if key == 'o':
            overlay = not overlay
        if key == 'p':
            increment_overlay(1)
        if key == 'i':
            increment_overlay(-1)
        if key == 'c':
            compensate = not compensate
        if key == 'b':
            brightness += 1
        if key == 'v':
            brightness += -1
        if key == 'w':
            windowy += -1
            cv2.moveWindow('feedback', windowx, windowy)
        if key == 's':
            windowy += 1
            cv2.moveWindow('feedback', windowx, windowy)
        if key == 'a':
            windowx += -1
            cv2.moveWindow('feedback', windowx, windowy)
        if key == 'd':
            windowx += 1
            cv2.moveWindow('feedback', windowx, windowy)
        if key == 'm':
            if trailing_average_weights:
                trailing_average_weights = []
                print("Trailing Averaging Disabled")
            else:
                trailing_average_weights = [.5, 0]
                print("Trailing Averaging enabled: ", trailing_average_weights)

        cv2.imshow('feedback', frame)


if __name__ == '__main__':
    main()
