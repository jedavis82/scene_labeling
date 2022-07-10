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
        annotation_results = model.get_image_annotations(name)

        print(f'{name} annotations:')
        for ar in annotation_results:
            print('Spatial relationship: ' + ar['spatial_relationship']
                  + '. General interaction: ' + ar['general_interaction'] + '. Person interaction: '
                  + ar['person_interaction'])
            arg_box = json.loads(ar['arg_bounding_box'])
            arg_label = ar['arg_label']
            ref_box = json.loads(ar['ref_bounding_box'])
            ref_label = ar['ref_label']
            draw_detection(image.copy(), [arg_box, ref_box], [arg_label, ref_label])
