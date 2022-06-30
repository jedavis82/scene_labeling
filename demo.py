"""
This demo script runs the scene annotation system on the input images located in ./input/demo_images/
"""
from scene_labeling import SceneLabeling
from utils import draw_detection
import cv2
import os
from tqdm import tqdm
import json

from spatial_relationships import SpatialRelationships

DEMO_IMAGES_DIR = './input/demo_images/'


def load_image_paths(img_dir=None):
    img_names = []
    img_paths = []
    for root, dirs, files in os.walk(img_dir):
        for f in files:
            img_path = img_dir + f
            img_paths.append(img_path)
            img_names.append(f)
    return img_names, img_paths


if __name__ == '__main__':
    model = SceneLabeling()
    image_names, image_paths = load_image_paths(DEMO_IMAGES_DIR)

    # Loop the image names in the demo dir and load them using OpenCV
    for name, path in tqdm(zip(image_names, image_paths), total=len(image_names)):
        image = cv2.imread(path, cv2.IMREAD_COLOR)

        # TODO: The object detection is working. Begin incorporating the spatial relationships into SceneLabeling
        model.process_image(image, name)
        det_results = model.get_object_detection_results(name)
        sr_results = model.get_spatial_relationship_results(name)
        for sr in sr_results:
            print(sr['spatial_relationship'])

        boxes = json.loads(det_results['bounding_boxes'])
        labels = json.loads(det_results['labels'])
        draw_detection(image, boxes, labels)
