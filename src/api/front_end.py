## Streamlit
import streamlit as st
import pika
import requests
from PIL import Image
import base64
import io
import cv2
import numpy as np

host = "localhost"
port = 5672
user = "guest"
password = "guest"
url = "http://localhost:8000"
upload = st.file_uploader("Upload a fundus image", type=["png", "jpg", "jpeg"])

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

run_id = st.text_input("Run ID")
if st.button("Load model"):
    resp = requests.get(url + "/model/" + run_id) 
    st.write(resp.content)
else:
    st.write("Click the button to load model.")

resp = requests.get(url + "/model/current") 
run_id = resp.content.decode("utf-8")
st.write(f"Current model: {run_id}")

if upload is not None:
    img = Image.open(upload)
    img = img.resize((200, 200))  # Resize the image to 200x200 pixels
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
                <img src="data:image/png;base64,{img_base64}" style="width: 150px; height: auto; margin: auto;"/>
            </div>
            <div style="text-align: center;">
                <p><b>Transformed Picture</b></p>
                <img src="data:image/png;base64,{preprocessed_img_base64}" style="width: 150px; height: auto; margin: auto;"/>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    image_bytes = upload.getvalue()
    st.write("Converted to bytes")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=pika.PlainCredentials(user, password)))
    channel = connection.channel()
    channel.queue_declare(queue="image")
    channel.basic_publish(exchange='', routing_key="image", body=image_bytes)
    resp = requests.get("http://localhost:8000/predict/image").json()
    # A predikciós érték alapján egy szöveges üzenet
    prediction_map = {
        1: "Healthy",
        2: "Mild Diabetic Retinopathy",
        3: "Moderate Diabetic Retinopathy",
        4: "Severe Diabetic Retinopathy",
        5: "Proliferative Diabetic Retinopathy"
    }

    # A predikció érték lekérése
    prediction_value = resp["prediction"][0]

    # Az érték alapján a megfelelő szöveg megjelenítése
    prediction_text = prediction_map.get(prediction_value, "Unknown Prediction")

    # A szöveges eredmény megjelenítése
    st.write("Prediction Result:", prediction_text)
    connection.close()
