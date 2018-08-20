from keras.applications import ResNet50, imagenet_utils
from keras.preprocessing.image import img_to_array
from PIL import Image
import tensorflow as tf
import numpy as np
model = None
graph = None

def load_model():
    # Load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras.
    global model
    model = ResNet50(weights='imagenet')
    global graph
    graph = tf.get_default_graph()


def prepare_image(image, target):
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image

