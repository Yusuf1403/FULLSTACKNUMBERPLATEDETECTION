import os

import cv2
import numpy as np
import matplotlib.pyplot as plt
import easyocr

from account.util import *
from PIL import Image


# define constants
model_cfg_path = 'C:\\Users\\AkshayAbhi\\OneDrive\\Desktop\\Dev\\NumberPlateDetection\\automatic-number-plate-recognition-python\\yolov3-from-opencv-object-detection\\model\\cfg\\darknet-yolov3.cfg'
model_weights_path = 'C:\\Users\\AkshayAbhi\\OneDrive\\Desktop\\Dev\\NumberPlateDetection\\automatic-number-plate-recognition-python\\yolov3-from-opencv-object-detection\\model\\weights\\model.weights'
class_names_path = 'C:\\Users\\AkshayAbhi\\OneDrive\\Desktop\\Dev\\NumberPlateDetection\\automatic-number-plate-recognition-python\\yolov3-from-opencv-object-detection\\model\\weights\\class.names'

input_dir = 'C:\\Users\\AkshayAbhi\\OneDrive\\Desktop\\Dev\\NumberPlateDetection\\automatic-number-plate-recognition-python\\data'


# for img_name in os.listdir(input_dir):
def ImageToText(img_path):
    # img_path = os.path.join(input_dir, img_name)

    # load class names
    with open('C:\\Users\\AkshayAbhi\\OneDrive\\Desktop\\Dev\\NumberPlateDetection\\automatic-number-plate-recognition-python\\yolov3-from-opencv-object-detection\\model\\weights\\class.names', 'r') as f:
        class_names = [j[:-1] for j in f.readlines() if len(j) > 2]
        f.close()

    # load model
    net = cv2.dnn.readNetFromDarknet(model_cfg_path, model_weights_path)

    # load image

    img = cv2.imread(img_path)

    H, W, _ = img.shape

    # convert image
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), True)

    # get detections
    net.setInput(blob)

    detections = get_outputs(net)

    # bboxes, class_ids, confidences
    bboxes = []
    class_ids = []
    scores = []

    for detection in detections:
        # [x1, x2, x3, x4, x5, x6, ..., x85]
        bbox = detection[:4]

        xc, yc, w, h = bbox
        bbox = [int(xc * W), int(yc * H), int(w * W), int(h * H)]

        bbox_confidence = detection[4]

        class_id = np.argmax(detection[5:])
        score = np.amax(detection[5:])

        bboxes.append(bbox)
        class_ids.append(class_id)
        scores.append(score)

    # apply nms
    bboxes, class_ids, scores = NMS(bboxes, class_ids, scores)

    # plot
    reader = easyocr.Reader(['en'])
    
    texts_detected = list()
    for bbox_, bbox in enumerate(bboxes):
        xc, yc, w, h = bbox

        """
        cv2.putText(img,
                    class_names[class_ids[bbox_]],
                    (int(xc - (w / 2)), int(yc + (h / 2) - 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    7,
                    (0, 255, 0),
                    15)
        """

        license_plate = img[int(yc - (h / 2)):int(yc + (h / 2)), int(xc - (w / 2)):int(xc + (w / 2)), :].copy()

        img = cv2.rectangle(img,
                            (int(xc - (w / 2)), int(yc - (h / 2))),
                            (int(xc + (w / 2)), int(yc + (h / 2))),
                            (0, 255, 0),
                            15)

        license_plate_gray = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)

        _, license_plate_thresh = cv2.threshold(license_plate_gray, 64, 255, cv2.THRESH_BINARY_INV)

        output = reader.readtext(license_plate_thresh)

        for out in output:
            text_bbox, text, text_score = out
            # if text_score > 0.4:
            print(text, text_score)
            texts_detected.append(text)

    print(texts_detected)
    plt.figure()
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    plt.figure()
    plt.imshow(cv2.cvtColor(license_plate, cv2.COLOR_BGR2RGB))

    plt.figure()
    plt.imshow(cv2.cvtColor(license_plate_gray, cv2.COLOR_BGR2RGB))

    data = cv2.cvtColor(license_plate_thresh, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(data, 'RGB')
    img.show()
    
    return texts_detected
    
    # return text 
