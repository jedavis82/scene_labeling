"""
This demo script runs the scene annotation system on the input images located in ./input/demo_images/
"""
from scene_labeling import SceneLabeling
from utils import draw_detection
import cv2
import os
import json

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
    for name, path in zip(image_names, image_paths):
        image = cv2.imread(path, cv2.IMREAD_COLOR)

        model.process_image(image, name)
        det_results = model.get_object_detection_results(name)
        metadata_results = model.get_metadata_results(name)
        annotation_results = model.get_image_annotations(name)

        print('Image Metadata:')
        md_labels = json.loads(metadata_results['labels'])
        md_confidences = json.loads(metadata_results['confidences'])
        for lab, conf in zip(md_labels, md_confidences):
            print(f'Label: {lab}. Confidence: {conf}')

        print('Image annotations:')
        for ar in annotation_results:
            print('Spatial relationship: ' + ar['spatial_relationship'] + '. General interaction: ' +
                  ar['general_interaction'] + '. Person interaction: ')

        boxes = json.loads(det_results['bounding_boxes'])
        labels = json.loads(det_results['labels'])
        draw_detection(image, boxes, labels)
