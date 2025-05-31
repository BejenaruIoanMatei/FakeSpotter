import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.inception_v3 import preprocess_input
from PIL import Image
import numpy as np

class TensorflowInceptionClassifier:
    def __init__(self):
        model_path = 'models/inception_fakespotter_tf_v2.h5'
        self.model = load_model(model_path)

    def preprocess(self, image_file):
        img = Image.open(image_file).convert("RGB").resize((299, 299))
        img_array = np.array(img).astype(np.float32)
        img_array = preprocess_input(img_array)
        return np.expand_dims(img_array, axis=0)

    def predict(self, image_file):
        try:
            input_tensor = self.preprocess(image_file)
            preds = self.model.predict(input_tensor)
            predicted_class = int(np.argmax(preds))
            confidence = float(np.max(preds))
            return {
                "label": "Real" if predicted_class == 1 else "Fake",
                "confidence": confidence,
                "probabilities": preds[0].tolist()
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return {
                "label": "Error",
                "confidence": 0.0,
                "error": str(e)
            }

classifier = TensorflowInceptionClassifier()
