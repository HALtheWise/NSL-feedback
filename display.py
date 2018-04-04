#!/usr/bin/env python3

import cv2

cap = cv2.VideoCapture(1)


def main():
    cv2.namedWindow('feedback')
    cv2.moveWindow('feedback', 600, 600)

    while True:
        ret, frame = cap.read()

        cv2.imshow('feedback', frame)

        key = chr(cv2.waitKey(1) & 0xFF)
        if key == 'q':
            # Quit if the "q" key is pressed over the window
            break
        if key == 's':
            # TODO: save the image
            pass


if __name__ == '__main__':
    main()
