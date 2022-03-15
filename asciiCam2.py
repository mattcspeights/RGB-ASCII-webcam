# import dependencies
import cv2
import math
import pyvirtualcam
import numpy as np

# define standard width and height of an ascii character
charWidth = 10
charHeight = 10

# defines camera object with input from standard webcam
cam = cv2.VideoCapture(0)

# sets max frame rate input from camera
cam.set(5, 30)

# checks if camera is successfully connected
if not cam.isOpened():
    raise IOError("Cannot Open Webcam")

# ascii characters arranged by darkness from light on the left to dark on the right
asciiList = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.                "

# loop through frames
with pyvirtualcam.Camera(width=950, height=620, fps=30) as outCam:
    while True:
        # unpack tuple from camera input
        ret, inputFrame = cam.read()

        # resize frame
        inputFrame = cv2.resize(inputFrame, (95, 62), interpolation=cv2.INTER_AREA)

        # creates a blank image
        blankFrame = np.zeros((len(inputFrame) * charHeight, len(inputFrame[0]) * charWidth, 3))

        # loop through image
        yCord = 0
        for line in inputFrame:
            xCord = 0
            for pixel in line:
                # grab color values
                r, g, b = pixel
                r = float(r)
                g = float(g)
                b = float(b)
                # get brightness of pixel
                brightness = (r + g + b) / 3

                # overlay ascii character based on brightness

                # render with normal colors
                cv2.putText(blankFrame, asciiList[len(asciiList) - 1 - math.floor(brightness / (255 / len(asciiList)))],
                            (xCord, yCord), cv2.FONT_HERSHEY_PLAIN, 1, (r/255, g/255, b/255), 1)

                # render with individually colored ascii characters
                # cv2.putText(blankFrame, asciiList[len(asciiList) - 1 - math.floor(r / (255 / len(asciiList)))],
                #             (xCord, yCord), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 1), 1)
                # cv2.putText(blankFrame, asciiList[len(asciiList) - 1 - math.floor(g / (255 / len(asciiList)))],
                #             (xCord, yCord), cv2.FONT_HERSHEY_PLAIN, 1, (0, 1, 0), 1)
                # cv2.putText(blankFrame, asciiList[len(asciiList) - 1 - math.floor(b / (255 / len(asciiList)))],
                            # (xCord, yCord), cv2.FONT_HERSHEY_PLAIN, 1, (1, 0, 0), 1)

                # increment by standard width
                xCord += charWidth

            # increment by standard height
            yCord += charHeight

        # create a preview of webcam feed
        cv2.imshow("video preview", blankFrame)

        # convert from float64 image to uint8 image
        blankFrame = (blankFrame * 255).astype(np.uint8)

        # output the frame to an obs virtual camera
        outCam.send(blankFrame)

        # frame rate normalization
        outCam.sleep_until_next_frame()

        #  press escape to end program
        c = cv2.waitKey(1)
        if c == 27:
            break

# ends webcam use
cam.release()

# closes the window for the image feed
cv2.destroyAllWindows()
