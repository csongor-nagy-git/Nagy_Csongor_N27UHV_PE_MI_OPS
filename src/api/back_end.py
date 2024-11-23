from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import mlflow
import mlflow.sklearn
import pandas as pd
import pika
import time
import logging

model = None
signature = None
app = FastAPI()

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


@app.get("/model/{run_id}")
def get_mlflow_model(run_id):
    global model, signature
    mlflow.set_tracking_uri("http://127.0.0.1:5000") 
    model_uri = f"runs:/{run_id}/model"
    model = mlflow.pyfunc.load_model(model_uri)
    client = mlflow.tracking.MlflowClient(tracking_uri="http://127.0.0.1:5000")
    return {"message": "Model loaded successfully!", "run_id": run_id}
#%% működik-e?

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("back_end:app", host="localhost", port=8000, reload=True)