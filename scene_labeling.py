"""
This class implements the scene labeling system.
The system will be separated into 3 parts
1. Object detection:
    Achieved by the YOLOv3 library
    Returns a list of object bounding boxes and labels found by the yolo library for an image
2. Object tuple spatial relationships
    Achieved by the GIOU and HOF algorithms
    Returns the proximity, overlap, and cardinal direction relationships for each tuple in an image
    Each of these outputs is represented as a fuzzy set.
    For the HOF output, the F0, F2, and Hybrid force histogram outputs are all returned
3. Scene annotations
    Achieved via the use of a FIS
    Returns tuple annotations in both the general and person domain (where applicable)
"""

from libs.object_detection import YoloObjectDetection
from libs.spatial_relationships import SpatialRelationships
from libs.metadata import MetaData
from libs.annotation.general import GeneralRules
from libs.annotation.person import PersonRules


class SceneLabeling:
    def __init__(self):
        self.__object_detection = YoloObjectDetection()
        self.__spatial_relationships = SpatialRelationships()
        self.__metadata = MetaData()
        self.__general_rules = GeneralRules()
        self.__person_rules = PersonRules()

        self.__object_detection_results = dict(dict())
        self.__metadata_results = dict(dict())
        self.__image_annotation_results = dict(dict())

    def process_image(self, image=None, image_name=None):
        assert image is not None, "Must supply an input image to process"
        assert image_name is not None, "Must supply an image name"

        # Compute the object localizations
        key, od_result = self.__object_detection.compute_detections(image, image_name)
        self.__object_detection_results[key] = od_result

        # Compute the image metadata
        meta = self.__metadata.compute_metadata(image)
        self.__metadata_results[key] = meta

        # Compute the spatial relationships
        key, sr_result = self.__spatial_relationships.compute_spatial_relationships(od_result, meta)
        self.__image_annotation_results[key] = sr_result

        # Compute the general interaction summaries
        key, general_annotation = self.__general_rules.compute_interactions(sr_result)
        self.__image_annotation_results[key] = general_annotation

        # Compute the person domain interaction summaries
        key, person_annotation = self.__person_rules.compute_interactions(sr_result)
        self.__image_annotation_results[key] = person_annotation

    def get_object_detection_results(self, key=None):
        """
        Return all object detection results if a key is not specified. Otherwise, return object detection results
        for the specific image
        :param key: None or relative path to image
        :return: Object detection results for image(s)
        """
        if key in self.__object_detection_results.keys():
            return self.__object_detection_results[key]
        else:
            return self.__object_detection_results

    def get_metadata_results(self, key=None):
        """
        Return all metadata results if a key is not specified. Otherwise
        return metadata results for a specific image
        :param key: None or relative path to image
        :return: Metadata results for image(s)
        """
        if key in self.__metadata_results.keys():
            return self.__metadata_results[key]
        else:
            return self.__metadata_results

    def get_image_annotations(self, key=None):
        """
        Return all spatial relationship results if a key is not specified. Otherwise, return spatial relationship
        results for a specific image
        :param key: None or relative path to image
        :return: Spatial relationship results for image(s)
        """
        if key in self.__image_annotation_results.keys():
            return self.__image_annotation_results[key]
        else:
            return self.__image_annotation_results
