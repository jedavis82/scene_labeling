"""
Use the inception library to compute image metadata
"""
import torch
from torchvision import models
import cv2
import numpy as np
import os
import json


class MetaData:
    def __init__(self,
                 labels_file='./input/labels/ilsvrc2012_wordnet_lemmas.txt',
                 torch_dir='./input/models/torchvision_models/resnet/'):
        # Constants used by the resnet model in torch
        os.environ['TORCH_HOME'] = torch_dir
        self.__mean = [0.485, 0.456, 0.406]
        self.__std = [0.229, 0.224, 0.225]
        self.__image_size = 224
        # Load the image net model. If it does not exist it will be
        # downloaded to the torch_dir directory
        self.__imagenet_labels = dict(enumerate(open(labels_file)))
        self.__model = models.resnet50(weights='ResNet50_Weights.DEFAULT')
        self.__model.to('cpu')
        self.__model.eval()

    def __preprocess_image(self, img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (self.__image_size, self.__image_size))
        image = image.astype("float32") / 255.0
        image /= self.__std
        image = np.transpose(image, (2, 0, 1))
        image = np.expand_dims(image, 0)
        return image

    def compute_metadata(self, img):
        image = self.__preprocess_image(img)
        image = torch.from_numpy(image)
        image = image.to('cpu')
        logits = self.__model(image)
        probabilities = torch.nn.Softmax(dim=1)(logits)
        sorted_probabilities = torch.argsort(probabilities, dim=1, descending=True)

        labels = []
        confidences = []
        for (_, idx) in enumerate(sorted_probabilities[0, :5]):
            _label = self.__imagenet_labels[idx.item()].strip()
            _conf = float(probabilities[0, idx.item()])
            labels.append(_label)
            confidences.append(_conf)
        results = {'labels': json.dumps(labels),
                   'confidences': json.dumps(confidences),
                   'num_labels': len(labels)}
        return results

