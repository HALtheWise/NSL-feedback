#!/usr/bin/env python3

import cv2
import numpy as np

cap = cv2.VideoCapture(1)


def main():
    cv2.namedWindow('feedback')
    cv2.moveWindow('feedback', 600, 600)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) 
    center = (int(width/2),int(height/2))
    markerrad = int(height/4)
    
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

    while True:
        ret, frame = cap.read()

        if downsample:
            # TODO: this
            
            pass

        if guide:
            # TODO: Clean up crosshair generation
            cv2.circle(frame, center, markerrad, (255,0,0), 2)
            cv2.drawMarker(frame, (center[0]+markerrad, center[1]),(0,0,255),cv2.MARKER_CROSS,20,2,cv2.FILLED)
            cv2.drawMarker(frame, (center[0]-markerrad, center[1]),(0,0,255),cv2.MARKER_CROSS,20,2,cv2.FILLED)
            cv2.drawMarker(frame, (center[0], center[1]+markerrad),(0,0,255),cv2.MARKER_CROSS,20,2,cv2.FILLED)
            cv2.drawMarker(frame, (center[0], center[1]-markerrad),(0,0,255),cv2.MARKER_CROSS,20,2,cv2.FILLED)
            pass

        if brightness != 0:
            bright = np.full_like(frame, abs(brightness))

            if brightness > 0:
                cv2.add(frame, bright, frame)
            else:
                cv2.subtract(frame, bright, frame)

        
        key = chr(cv2.waitKey(1) & 0xFF)
        if key == 'q':
            # Quit if the "q" key is pressed over the window
            break
        if key == 's':
            # TODO: save the image
            pass
        if key == 'd':
            downsample = not downsample
        if key == 'g':
            guide = not guide

        cv2.imshow('feedback', frame)


if __name__ == '__main__':
    main()
