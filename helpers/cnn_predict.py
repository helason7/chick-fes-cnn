from PIL import Image
import io
import numpy as np
import tensorflow as tf

from config.config import CNN_INPUT_SIZE


cnn_model = None

def is_cnn_loaded():
    return cnn_model is not None

def load_cnn():
    global cnn_model
    cnn_model = tf.keras.models.load_model("model/cnn_model.h5")


def predict_disease(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(CNN_INPUT_SIZE)

    x = np.array(image) / 255.0
    x = np.expand_dims(x, axis=0)

    preds = cnn_model.predict(x)[0]

    class_idx = int(np.argmax(preds))
    confidence = float(np.max(preds))

    return class_idx, confidence
