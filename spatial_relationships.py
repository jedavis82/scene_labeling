"""
This class will compute the proximity and overlap between an object tuple using GIOU.
Additionally, the cardinal direction will be computed using the HOF algorithm.
"""
import json
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from sklearn.preprocessing import minmax_scale
import hofpy
from utils import convert_boxes, get_image_tuples
import cv2


def compute_giou(arg_box=None, ref_box=None):
    assert arg_box is not None, "Must supply argument image box"
    assert ref_box is not None, "Must supply referrant image box"
    arg_x1 = arg_box[0]
    arg_y1 = arg_box[1]
    arg_x2 = arg_box[2]
    arg_y2 = arg_box[3]
    area_arg_obj = (arg_x2 - arg_x1) * (arg_y2 - arg_y1)
    # Compute the area of the ref obj
    ref_x1 = ref_box[0]
    ref_y1 = ref_box[1]
    ref_x2 = ref_box[2]
    ref_y2 = ref_box[3]
    area_ref_obj = (ref_x2 - ref_x1) * (ref_y2 - ref_y1)

    # Calculate the intersection between the arg and ref objects
    x_1_I = max(arg_x1, ref_x1)
    x_2_I = min(arg_x2, ref_x2)
    y_1_I = max(arg_y1, ref_y1)
    y_2_I = min(arg_y2, ref_y2)
    if x_2_I > x_1_I and y_2_I > y_1_I:  # Double check this, I think and is correct here.
        I = (x_2_I - x_1_I) * (y_2_I - y_1_I)
    else:
        I = 0

    # Find the coordinates of the smallest bounding box that encloses both objects
    x_1_c = min(ref_x1, arg_x1)
    x_2_c = max(ref_x2, arg_x2)
    y_1_c = min(ref_y1, arg_y1)
    y_2_c = max(ref_y2, arg_y2)

    # Calculate the area of the smallest enclosing bounding box
    area_b_c = (x_2_c - x_1_c) * (y_2_c - y_1_c)

    # Calculate the IOU (Intersection over Union)
    # IoU = I/U, where U = Area_ref + Area_arg - I
    U = area_arg_obj + area_ref_obj - I
    IoU = I / U

    # Calculate GIoU (Generalized Intersection over Union)
    # GIoU = IoU - (Area_c - U)/Area_c
    GIoU = IoU - ((area_b_c - U) / area_b_c)
    return GIoU, IoU


def compute_hof(arg_object=None, ref_object=None, num_directions=360):
    """
        Compute HOF for an object tuple and return the max angles for F0, F2, and Hybrid
        :param arg_object: A binary mask image representing the argument object
        :param ref_object: A binary mask image representing the referrant object
        :param num_directions: The number of histogram of forces directions to compute (default 360)
        :return: The maximum F0, F2, and Hybrid HOF angles
        """
    assert arg_object is not None, "Must supply argument image"
    assert ref_object is not None, "Must supply referrant image"
    f0 = hofpy.F0Hist(arg_object, ref_object, numberDirections=num_directions)
    f2 = hofpy.F2Hist(arg_object, ref_object, numberDirections=num_directions)
    hybrid = hofpy.F02Hist(arg_object, ref_object, numberDirections=num_directions)

    f0 = np.nan_to_num(f0)
    f2 = np.nan_to_num(f2)
    hybrid = np.nan_to_num(hybrid)
    max_f0_angle = np.argmax(f0)
    max_f2_angle = np.argmax(f2)
    max_hybrid_angle = np.argmax(hybrid)
    return max_f0_angle, max_f2_angle, max_hybrid_angle


def compute_hof_display(arg_object=None, ref_object=None, num_directions=360):
    """
    Compute HOF for an object two-tuple and return the histograms for display
    :param arg_object:
    :param ref_object:
    :param num_directions:
    :return:
    """
    assert arg_object is not None, "Must supply the argument mask image"
    assert ref_object is not None, "Must supply the referrant mask image"
    f0 = hofpy.F0Hist(arg_object, ref_object, numberDirections=num_directions)
    f2 = hofpy.F2Hist(arg_object, ref_object, numberDirections=num_directions)
    hybrid = hofpy.F02Hist(arg_object, ref_object, numberDirections=num_directions)
    f0 = np.nan_to_num(f0)
    f2 = np.nan_to_num(f2)
    hybrid = np.nan_to_num(hybrid)
    f0_histograms = minmax_scale(f0, feature_range=(0, 100))
    f2_histograms = minmax_scale(f2, feature_range=(0, 100))
    hyb_histograms = minmax_scale(hybrid, feature_range=(0, 100))

    return f0_histograms.astype(int), f2_histograms.astype(int), hyb_histograms.astype(int)


class Defuzz:
    def __init__(self):
        self.overlap = ctrl.Antecedent(universe=np.arange(-1.1, 1.1, 0.1), label='overlap')
        self.sr = ctrl.Antecedent(universe=np.arange(-1, 361, 1), label='spatial_relationships')

        self.overlap['Overlap'] = fuzz.trapmf(self.overlap.universe, [0.0, 0.2, 0.7, 1.0])
        self.overlap['No Overlap'] = fuzz.trapmf(self.overlap.universe, [-1.0, -0.7, -0.2, 0.0])

        # 0 < HOF < 30 | 331 < HOF < 360: Right
        self.sr['Right1'] = fuzz.trimf(self.sr.universe, [-1, 15, 31])
        self.sr['Right2'] = fuzz.trimf(self.sr.universe, [330, 345, 360])
        # 31 < HOF < 60: Above Right
        self.sr['Above Right'] = fuzz.trimf(self.sr.universe, [30, 45, 61])
        # 61 < HOF < 120: Above
        self.sr['Above'] = fuzz.trimf(self.sr.universe, [60, 90, 121])
        # 121 < HOF < 150: Above Left
        self.sr['Above Left'] = fuzz.trimf(self.sr.universe, [120, 135, 151])
        # 151 < HOF < 210: Left
        self.sr['Left'] = fuzz.trimf(self.sr.universe, [150, 180, 211])
        # 211 < HOF < 240: Below Left
        self.sr['Below Left'] = fuzz.trimf(self.sr.universe, [210, 225, 241])
        # 241 < HOF < 300: Below
        self.sr['Below'] = fuzz.trimf(self.sr.universe, [240, 270, 301])
        # 301 < HOF < 330: Below Right
        self.sr['Below Right'] = fuzz.trimf(self.sr.universe, [300, 315, 331])

    def defuzzify_results(self, iou, sr_angle):
        # Compute the overlap result
        overlap = fuzz.interp_membership(self.overlap.universe, self.overlap['Overlap'].mf, iou)
        no_overlap = fuzz.interp_membership(self.overlap.universe, self.overlap['No Overlap'].mf, iou)
        membership = {'Overlap': overlap, 'No Overlap': no_overlap}
        overlap_label = max(membership, key=membership.get)

        # Compute the spatial relationship result
        right_1 = fuzz.interp_membership(self.sr.universe, self.sr['Right1'].mf, sr_angle)
        right_2 = fuzz.interp_membership(self.sr.universe, self.sr['Right2'].mf, sr_angle)
        above_right = fuzz.interp_membership(self.sr.universe, self.sr['Above Right'].mf, sr_angle)
        above = fuzz.interp_membership(self.sr.universe, self.sr['Above'].mf, sr_angle)
        above_left = fuzz.interp_membership(self.sr.universe, self.sr['Above Left'].mf, sr_angle)
        left = fuzz.interp_membership(self.sr.universe, self.sr['Left'].mf, sr_angle)
        below_left = fuzz.interp_membership(self.sr.universe, self.sr['Below Left'].mf, sr_angle)
        below = fuzz.interp_membership(self.sr.universe, self.sr['Below'].mf, sr_angle)
        below_right = fuzz.interp_membership(self.sr.universe, self.sr['Below Right'].mf, sr_angle)
        membership = {'Right1': right_1, 'Right2': right_2, 'Above Right': above_right, 'Above': above,
                      'Above Left': above_left, 'Left': left, 'Below Left': below_left, 'Below': below,
                      'Below Right': below_right}
        sr_label = max(membership, key=membership.get)
        if sr_label == 'Right1' or sr_label == 'Right2':
            sr_label = 'Right'
        return overlap_label, sr_label


class SpatialRelationships:
    def __init__(self,
                 animate_objects_file='./input/animate_objects.csv'):
        """
        Compute the proximity, overlap, and cardinal directions between object tuples in an image
        :param animate_objects_file: File containing a list of animate objects in the data set
        """
        assert animate_objects_file is not None, "Must supply animate objects file"

        self.__animate_objects = list(pd.read_csv(animate_objects_file, encoding='utf-8', engine='python')['object'])
        self.__defuzzer = Defuzz()
        self.__direction_lookup = {
            'Right': 'is to the right of',
            'Above Right': 'is above and to the right of',
            'Above': 'is above',
            'Above Left': 'is above and to the left of',
            'Left': 'is to the left of',
            'Below Left': 'is below and to the left of',
            'Below': 'is below',
            'Below Right': 'is below and to the right of'
        }

    def __order_arg_ref_pair(self, arg_label, ref_label):
        """
        Order the labels for the tuple according to person -> animate -> inanimate
        :param arg_label:
        :param ref_label:
        :return:
        """
        al_split = '_'.join(arg_label.split('_')[:-1])
        rl_split = '_'.join(ref_label.split('_')[:-1])

        # People always take precedent
        if al_split == 'person':
            return arg_label, ref_label
        if rl_split == 'person':
            return ref_label, arg_label
        # Animate objects take precedent over inanimate objects
        if al_split in self.__animate_objects:
            return arg_label, ref_label
        if rl_split in self.__animate_objects:
            return ref_label, arg_label
        # Both are inanimate objects
        else:
            return arg_label, ref_label

    def __get_concensus_angle(self, f0, f2, hyb):
        if f0 == f2:
            return f0
        if f0 == hyb:
            return hyb
        if f2 == hyb:
            return hyb
        else:
            return hyb

    def __construct_spatial_relationships(self, arg_label, ref_label, overlap_label, sr_label):
        direction = self.__direction_lookup[sr_label]
        if overlap_label == 'Overlap':
            return f'{arg_label} overlaps and {direction} {ref_label}'
        else:
            return f'{arg_label} {direction} {ref_label}'

    def compute_giou(self, arg_box=None, ref_box=None):
        assert arg_box is not None, "Must supply argument image box"
        assert ref_box is not None, "Must supply referrant image box"
        arg_x1 = arg_box[0]
        arg_y1 = arg_box[1]
        arg_x2 = arg_box[2]
        arg_y2 = arg_box[3]
        area_arg_obj = (arg_x2 - arg_x1) * (arg_y2 - arg_y1)
        # Compute the area of the ref obj
        ref_x1 = ref_box[0]
        ref_y1 = ref_box[1]
        ref_x2 = ref_box[2]
        ref_y2 = ref_box[3]
        area_ref_obj = (ref_x2 - ref_x1) * (ref_y2 - ref_y1)

        # Calculate the intersection between the arg and ref objects
        x_1_I = max(arg_x1, ref_x1)
        x_2_I = min(arg_x2, ref_x2)
        y_1_I = max(arg_y1, ref_y1)
        y_2_I = min(arg_y2, ref_y2)
        if x_2_I > x_1_I and y_2_I > y_1_I:  # Double check this, I think and is correct here.
            I = (x_2_I - x_1_I) * (y_2_I - y_1_I)
        else:
            I = 0

        # Find the coordinates of the smallest bounding box that encloses both objects
        x_1_c = min(ref_x1, arg_x1)
        x_2_c = max(ref_x2, arg_x2)
        y_1_c = min(ref_y1, arg_y1)
        y_2_c = max(ref_y2, arg_y2)

        # Calculate the area of the smallest enclosing bounding box
        area_b_c = (x_2_c - x_1_c) * (y_2_c - y_1_c)

        # Calculate the IOU (Intersection over Union)
        # IoU = I/U, where U = Area_ref + Area_arg - I
        U = area_arg_obj + area_ref_obj - I
        IoU = I / U

        # Calculate GIoU (Generalized Intersection over Union)
        # GIoU = IoU - (Area_c - U)/Area_c
        GIoU = IoU - ((area_b_c - U) / area_b_c)
        return GIoU, IoU

    def compute_spatial_relationships(self, object_detection_results=None):
        """
        :param object_detection_results:
        :return:
        """
        assert object_detection_results is not None, "Must supply image's object detection results"

        # Return a list of dictionaries as the result for this image
        image_results = list(dict())
        boxes = convert_boxes(object_detection_results['bounding_boxes'])
        labels = json.loads(object_detection_results['labels'])
        img_width = object_detection_results['img_width']
        img_height = object_detection_results['img_height']
        rel_path = object_detection_results['key']
        # Map the bounding boxes to their corresponding labels for use when computing spatial relationships
        label_box_map = {}
        for box, label in zip(boxes, labels):
            label_box_map[label] = box

        img_tuples = get_image_tuples(img_labels=labels)
        img_name = rel_path.rsplit('.', 1)[0]  # Remove the file extension to use for a key
        for tup in img_tuples:
            arg_label, ref_label = self.__order_arg_ref_pair(tup[0], tup[1])
            arg_box = label_box_map[arg_label]
            ref_box = label_box_map[ref_label]
            key = f'{img_name}_{arg_label}_{ref_label}'

            giou, iou = compute_giou(arg_box, ref_box)

            # Create two binary mask images that correspond to the arg and ref boxes for use with HOF
            arg_hof = np.zeros((img_height, img_width), dtype='uint8')
            ref_hof = np.zeros((img_height, img_width), dtype='uint8')
            arg_hof[arg_box[1]:arg_box[3], arg_box[0]:arg_box[2]] = 255
            ref_hof[ref_box[1]:ref_box[3], ref_box[0]:ref_box[2]] = 255

            # Testing the np images are constructed correctly
            # img_path = f'./input/demo_images/{rel_path}'
            # orig_img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
            # cv2.rectangle(orig_img, (arg_box[0], arg_box[1]), (arg_box[2], arg_box[3]), (255, 0, 0), 2)
            # cv2.rectangle(orig_img, (ref_box[0], ref_box[1]), (ref_box[2], ref_box[3]), (0, 255, 0), 2)
            # cv2.imshow('Original image', orig_img)
            # cv2.imshow('Arg object', arg_hof)
            # cv2.imshow('Ref object', ref_hof)
            # cv2.waitKey(0)

            f0, f2, hybrid = compute_hof(arg_hof, ref_hof)
            sr_angle = self.__get_concensus_angle(f0, f2, hybrid)

            overlap_label, sr_label = self.__defuzzer.defuzzify_results(iou, sr_angle)
            img_summary = self.__construct_spatial_relationships(arg_label, ref_label, overlap_label, sr_label)
            img_summary_result = {
                'key': key, 'relative_path': rel_path, 'img_name': img_name, 'arg_label': arg_label,
                'arg_bounding_box': json.dumps(arg_box), 'ref_label': ref_label,
                'ref_bounding_box': json.dumps(ref_box), 'overlap': iou, 'proximity': giou,
                'f0': f0, 'f2': f2, 'hybrid': hybrid, 'spatial_relationship': img_summary
            }
            image_results.append(img_summary_result)
        return rel_path, image_results
