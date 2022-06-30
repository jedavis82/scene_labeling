"""
This class implements YOLOv3 object detection.
The default arguments for the class are what were used during testing of the S2T system.
The class will take an image as input and return the bounding boxes and labels for each object in the image.

Based on code similar to here: https://opencv-tutorial.readthedocs.io/en/latest/yolo/yolo.html
"""

import cv2
import numpy as np
import json
from utils import load_label_map


class YoloObjectDetection:
    def __init__(self,
                 model_file='./input/models/yolo/yolov3.cfg',
                 weights_file='./input/models/yolo/yolov3.weights',
                 labels_file='./input/labels/coco.names',
                 box_confidence_threshold=0.79,
                 nms_threshold=0.4,
                 input_width=416,
                 input_height=416
                 ):
        self.__yolo_model = cv2.dnn.readNetFromDarknet(model_file, weights_file)
        self.__yolo_model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

        # Grab the layer names from the unconnected output layers so the class can be extracted
        self.__layer_names = self.__yolo_model.getLayerNames()
        self.__layer_names = [self.__layer_names[i - 1] for i in self.__yolo_model.getUnconnectedOutLayers()]

        self.__box_confidence_threshold = box_confidence_threshold
        self.__nms_threshold = nms_threshold
        self.__input_width = input_width
        self.__input_height = input_height

        self.__labels_dict = load_label_map(labels_file)

    def compute_detections(self, image=None, image_key=None):
        """
        Perform YOLOv3 object detection on an image
        :param image: The input image to process
        :param image_key: A lookup key for the returned results. Usually the image path
        :return: Dictionary containing the object detection results for the input image
        """
        assert image is not None, "Must supply input image"
        assert image_key is not None, "Must supply image key for future lookup. Usually relative path of the image"

        blob = cv2.dnn.blobFromImage(image, 1/255, (self.__input_width, self.__input_height), [0, 0, 0], 1, crop=False)
        self.__yolo_model.setInput(blob)
        outs = self.__yolo_model.forward(self.__layer_names)

        img_height = image.shape[0]
        img_width = image.shape[1]

        class_ids = []
        confidences = []
        boxes = []

        json_boxes = []
        json_labels = []
        json_confidences = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.__box_confidence_threshold:
                    center_x = int(detection[0] * img_width)
                    center_y = int(detection[1] * img_height)
                    width = int(detection[2] * img_width)
                    height = int(detection[3] * img_height)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    # Prevent negative coords
                    x = max(0, left)
                    y = max(0, top)
                    right = max(0, (left + width))
                    bottom = max(0, (top + height))
                    boxes.append([x, y, right, bottom])
        # Perform NMS to eliminate redundant overlapping bounding boxes with lower confidences
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.__box_confidence_threshold, self.__nms_threshold)
        obj_labels = {}
        for idx in indices:
            box = boxes[idx]
            conf = confidences[idx]
            label = self.__labels_dict[int(class_ids[idx])]
            # Don't allow duplicate labels, instead use a sequential numbering scheme for like objects
            if label not in obj_labels:
                obj_labels[label] = 1
            else:
                obj_labels[label] += 1
            obj_label = label + '_' + str(obj_labels[label])
            json_labels.append(obj_label)
            json_boxes.append(box)
            json_confidences.append(conf)
        num_objects = len(indices)
        img_result = {'key': image_key, 'num_objects': num_objects, 'bounding_boxes': json.dumps(json_boxes),
                      'confidences': json.dumps(json_confidences), 'labels': json.dumps(json_labels),
                      'img_width': img_width, 'img_height': img_height}
        return image_key, img_result
