"""
This script contains various helper functions for the library
"""
import cv2
import numpy as np
import json
from itertools import permutations


def load_label_map(labels_file):
    labels_dict = {}
    with open(labels_file, 'r') as lmf:
        i = 0
        for line in lmf:
            labels_dict[i] = line.replace(' ', '_').rstrip('\n')
            i += 1
    return labels_dict


def convert_boxes(json_boxes):
    ret_boxes = []
    boxes = np.array(json.loads(json_boxes))
    for b in boxes:
        x = b[0]
        y = b[1]
        right = b[2]
        bottom = b[3]
        # Must convert from numpy int32 data type to python's int or the matlab engine will throw an error
        ret_boxes.append([int(x), int(y), int(right), int(bottom)])
    return ret_boxes


def get_image_tuples(img_labels=None):
    """
    Compute the list of tuples between objects in an image
    :param img_labels: The list of labels for the corresponding image
    :return: The permutated list of tuples in the image
    """
    tuples = list(permutations(img_labels, 2))
    no_inverse_tuples = []
    no_inverse_key = []
    for tup in tuples:
        check = tup[1] + tup[0]
        if check in no_inverse_key:
            continue  # No processing inverse relationships
        no_inverse_tuples.append(tup)
        no_inverse_key.append(tup[0] + tup[1])
    return no_inverse_tuples


def get_consensus_angle(f0, f2, hyb):
    if f0 == f2:
        return f0
    if f0 == hyb:
        return hyb
    if f2 == hyb:
        return hyb
    else:
        return hyb


def convert_meta_labels(labels):
    for l in labels:
        if l == 'soccer_ball' or l == 'tennis_ball' or l == 'baseball':
            return l
    else:
        return labels[0]


def draw_detection(img, boxes, labels):
    for box, label in zip(boxes, labels):
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
        cv2.putText(img, label, (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
    cv2.imshow("Bounding Box Output", img)
    cv2.waitKey(0)
