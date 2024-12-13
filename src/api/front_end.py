## Streamlit
import streamlit as st
import pika
import requests
from PIL import Image
import base64
import io
import cv2
import numpy as np
import tensorflow as tf
import os

host = "localhost"
port = 5672
user = "guest"
password = "guest"
url = "http://localhost:8000"
saved_models_dir = "saved_models"  # Directory where Keras models are stored

# Global variable to store the model
if 'model' not in st.session_state:
    st.session_state.model = None

def ben_graham_preprocessing(image):
    """Applies Ben Graham preprocessing with enhanced color preservation."""
    # Convert PIL Image to NumPy Array
    img = np.array(image)

    # Rescale image to a fixed radius
    def scale_radius(img, scale=300):
        x = img[img.shape[0] // 2, :, :].sum(1)
        r = (x > x.mean() / 10).sum() // 2
        s = scale * 1.0 / r
        return cv2.resize(img, None, fx=s, fy=s)

    img = scale_radius(img, scale=300)

    # Subtract local average color
    blur = cv2.GaussianBlur(img, (0, 0), 10)
    img = cv2.addWeighted(img, 4, blur, -4, 128)

    # Boost color saturation and contrast
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.5, 0, 255)  # Boost saturation
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.2, 0, 255)  # Brightness adjustment
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    # Remove outer 10%
    mask = np.zeros(img.shape, dtype=np.uint8)
    cv2.circle(mask, (img.shape[1] // 2, img.shape[0] // 2), int(0.9 * 300), (1, 1, 1), -1, 8, 0)
    img = img * mask + 128 * (1 - mask)

    # Convert back to PIL Image
    return Image.fromarray(img)

# Load Keras model
def load_keras_model(model_name):
    """Loads a Keras model from the saved_models directory."""
    model_path = os.path.join(saved_models_dir, model_name)
    if os.path.exists(model_path):
        return tf.keras.models.load_model(model_path)
    else:
        st.error("Model not found. Please check the name and try again.")
        return None

# Map severities to labels
severity_labels = {
    0: "No Diabetic Retinopathy",
    1: "Mild Diabetic Retinopathy",
    2: "Moderate Diabetic Retinopathy",
    3: "Severe Diabetic Retinopathy",
    4: "Proliferative Diabetic Retinopathy"
}

# Title of the application
st.title("Diabetic Retinopathy Detection")

# Model selection section below the title
st.header("Load a Keras Model")
model_name = st.text_input("Enter the Keras model name (e.g., model.h5):")
if st.button("Load Model"):
    st.session_state.model = load_keras_model(model_name)
    if st.session_state.model:
        st.success(f"Model '{model_name}' loaded successfully!")

# File upload section
st.header("Upload a fundus image")
upload = st.file_uploader("Please make sure that it has a good quality!", type=["png", "jpg", "jpeg"], key="fundus_image_upload")

if upload is not None:
    img = Image.open(upload)
    img = img.resize((224, 224))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Apply Ben Graham preprocessing
    preprocessed_img = ben_graham_preprocessing(img)
    buffered_preprocessed = io.BytesIO()
    preprocessed_img.save(buffered_preprocessed, format="PNG")
    preprocessed_img_base64 = base64.b64encode(buffered_preprocessed.getvalue()).decode('utf-8')

    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; gap: 20px;">
            <div style="text-align: center;">
                <p><b>Original Picture</b></p>
                <img src="data:image/png;base64,{img_base64}" style="width: 300px; height: auto; margin: auto;"/>
            </div>
            <div style="text-align: center;">
                <p><b>Transformed Picture</b></p>
                <img src="data:image/png;base64,{preprocessed_img_base64}" style="width: 300px; height: auto; margin: auto;"/>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Predict using the loaded model
    if st.session_state.model:
        try:
            with st.spinner("Running prediction..."):
                preprocessed_img = preprocessed_img.resize((224, 224))  # Resize for Keras input
                img_array = np.array(preprocessed_img).astype('float32')
                img_array = np.expand_dims(img_array, axis=0)

                prediction = st.session_state.model.predict(img_array)[0][0]  # Single value prediction
                rounded_prediction = round(prediction)  # Round the value to nearest integer
                clipped_prediction = np.clip(rounded_prediction, 0, 4)
                label = severity_labels.get(clipped_prediction, "Unknown Severity")

            st.write("\n")
            st.success(f"Prediction Result: {label}")
        except Exception as e:
            st.error(f"Error during prediction: {str(e)}")
    else:
        st.warning("Please load a model before running predictions.")