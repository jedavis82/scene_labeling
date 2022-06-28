"""
Use the fiftyone library to load the train and validation COCO 2017 sets.
Combine the images into one directory, we will be using YOLOv3 to generate object detections
"""

import fiftyone as fo
import fiftyone.zoo as foz
import os
import shutil

DATASET_DIR = './'
TRAIN_DIR = DATASET_DIR + 'coco-2017/train/data/'
VAL_DIR = DATASET_DIR + 'coco-2017/validation/data/'
OUTPUT_DIR = DATASET_DIR + 'coco_images/'

if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def main():
    fo.config.dataset_zoo_dir = DATASET_DIR  # Specify the output directory of the downloaded files

    print(fo.config)  # Verify the settings were updated correctly

    dataset = foz.load_zoo_dataset(
        "coco-2017",
        splits=["train", "validation"],
        classes=["person"],
        label_types="detections",
        max_samples=2000,
        include_license=False
    )

    # Combine the training and validation images into one directory. Remove the JSON annotated files.
    # This code performs object detection using YOLOv3 and does not rely on the annotations
    train_images = os.listdir(TRAIN_DIR)
    val_images = os.listdir(VAL_DIR)
    for f in train_images:
        shutil.move(os.path.join(TRAIN_DIR, f), OUTPUT_DIR)
    for f in val_images:
        shutil.move(os.path.join(VAL_DIR, f), OUTPUT_DIR)

    # Clean up the downloaded annotation files
    shutil.rmtree(DATASET_DIR + 'coco-2017/')


if __name__ == '__main__':
    main()
