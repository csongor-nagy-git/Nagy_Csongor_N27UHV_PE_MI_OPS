## Streamlit
import streamlit as st
import pika
import requests
from PIL import Image

host = "localhost"
port = 5672
user = "guest"
password = "guest"
url = "http://localhost:8000"
upload = st.file_uploader("Upload a fundus image", type=["png", "jpg", "jpeg"])


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
    st.image(img, caption="Uploaded Image", use_container_width=True)
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