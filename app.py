
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import base64
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


app = FastAPI(title="Chicken Disease Predictor")

# Load the trained model
# Load pickled model
# with open('model_cnn.pkl', 'rb') as file:
#     model = pickle.load(file)
model = load_model("cnn_model.h5")

IMG_SIZE = (150, 150)
CLASS_NAMES = ["coccidiosis", "healthy", "new_castle_disease", "salmonella"]


def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(IMG_SIZE)
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


@app.get("/")
def root(): 
    print("Chicken Disease Predictor is running.")
    return {"message": "Chicken Disease Predictor is running."}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = preprocess_image(image_bytes)

        predictions = model.predict(image)
        confidence = float(np.max(predictions))
        class_index = int(np.argmax(predictions))
        class_name = CLASS_NAMES[class_index]

        return {
            "class_index": class_index,
            "class": class_name,
            "confidence": round(confidence, 4)
        }

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

    try:
        # Decode base64 image
        image_data = base64.b64decode(request.image)
        pil_image = Image.open(io.BytesIO(image_data))

        # Class names
        class_names = ['Coccidiosis', 'Healthy', 'New Castle Disease', 'Salmonella']

        predicted_class, confidence, probabilities = predict_disease(pil_image, model, class_names)

        return {
            "predicted_class": predicted_class,
            "confidence": float(confidence),
            "probabilities": probabilities.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))