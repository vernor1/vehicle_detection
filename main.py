import argparse
import cv2
import numpy as np

from classifier import TClassifier
from moviepy.editor import VideoFileClip
from vehicle_tracker import TVehicleTracker


# Global Variables ------------------------------------------------------------
Classifier = TClassifier("vehicles", "non-vehicles")
Tracker = TVehicleTracker(Classifier, (380, 660))

# Functions ------------------------------------------------------------
def ProcessImage(img):
    """ Processes an RGB image for detecting vehicles.
        The information is added to the original image in overlay.

    param: img: Image to process
    returns: Processed RGB image
    """

    # Convert the RGB image of MoviePy to BGR format of OpenCV
    outImg = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # Process image and add overlay if any vehicles are detected
    Tracker.ProcessImage(outImg)
    vehicleIds, boundingBoxes = Tracker.GetVehicles()
    for idx in range(len(vehicleIds)):
        boxLeftTop = boundingBoxes[idx][0][0], boundingBoxes[idx][0][1]
        boxRightBottom = boundingBoxes[idx][1][0], boundingBoxes[idx][1][1]
        cv2.rectangle(outImg, boxLeftTop, boxRightBottom, (0, 255, 255), 2)
        cv2.putText(outImg, "Vehicle %d" % (vehicleIds[idx]),
                    (boxLeftTop[0]+5, boxLeftTop[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
    # Convert the processed image back to the RGB format comatible with MoviePy
    outImg = cv2.cvtColor(outImg, cv2.COLOR_BGR2RGB)
    return outImg

if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="Main Pipeline")
    argParser.add_argument("in_clip", type=str, help="Path to the original clip")
    argParser.add_argument("out_clip", type=str, help="Path to the clip with the vehicle overlay")
    args = argParser.parse_args()
    inClip = VideoFileClip(args.in_clip)
    outClip = inClip.fl_image(ProcessImage)
    outClip.write_videofile(args.out_clip, audio=False)
