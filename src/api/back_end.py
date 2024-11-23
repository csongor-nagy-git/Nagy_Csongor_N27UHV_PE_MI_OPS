from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import JSONResponse
import mlflow
import mlflow.sklearn
from PIL import Image
import pandas as pd
import pika
import time
import logging
import numpy as np
import io

model = None
client = None
signature = None
rabbit_connection = None
channel = None
current_run_id = None

app = FastAPI()

def process_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    img = np.array(img)  # Átalakítjuk numpy tömbbé
    img = np.expand_dims(img, axis=0)  # Bemeneti formátum a modellekhez
    return img

def predict_from_image(image_bytes):
    img = process_image(image_bytes)
    prediction = model.predict(img)
    return prediction

def on_request(ch, method, properties, body):
    print("Received image for prediction")
    prediction = predict_from_image(body)
    
    # Válasz küldése RabbitMQ-ba
    ch.basic_publish(exchange='',routing_key=properties.reply_to,properties=pika.BasicProperties(correlation_id=properties.correlation_id),body=str(prediction))

    ch.basic_ack(delivery_tag=method.delivery_tag)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, rabbit_connection, channel
    client = mlflow.tracking.MlflowClient(tracking_uri="http://127.0.0.1:5000")
    credentials = pika.PlainCredentials(username="guest", password="guest")
    while rabbit_connection is None:
        try:
            rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host = "localhost", port = 5672, credentials=credentials, heartbeat=0))
        except pika.exceptions.AMQPConnectionError:
            logging.error(f"Connection to RabbitMQ failed at localhost:5672. Retrying...")
            time.sleep(0.3)
    channel = rabbit_connection.channel()
    channel.basic_qos(prefetch_count=1)
                
    yield
    channel.close()
    rabbit_connection.close()
    return

app = FastAPI(lifespan=lifespan)

@app.get("/") 
async def read_root():
    """Default path. See /docs for more."""
    return "Hello World"

@app.get("/model/current")
def get_model_state():
    global current_run_id

    if current_run_id is None:
        return "No model is loaded"
    else:
        return current_run_id 

@app.get("/model/{run_id}")
def get_mlflow_model(run_id):
    global model, signature, current_run_id
    mlflow.set_tracking_uri("http://127.0.0.1:5000") 
    model_uri = f"runs:/{run_id}/model"
    model = mlflow.pyfunc.load_model(model_uri)
    client = mlflow.tracking.MlflowClient(tracking_uri="http://127.0.0.1:5000")
    current_run_id = run_id
    return {"message": "Model loaded successfully!", "run_id": run_id}
#%% működik-e?

@app.get("/predict/{queue}")
async def predict(queue: str):
    global channel
    method_frame, header_frame, body = channel.basic_get(queue)
    data = body
    channel.basic_ack(method_frame.delivery_tag)
    prediction = predict_from_image(data)
    
    # Eredmény visszaküldése
    return {"prediction": prediction.tolist()}  # Átalakítjuk listává, hogy JSON-ban visszaadható legyen


if __name__ == "__main__":
    import threading
    import uvicorn

    uvicorn.run("back_end:app", host="localhost", port=8000, reload=True)