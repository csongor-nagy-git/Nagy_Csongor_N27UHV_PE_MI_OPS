import mlflow
import mlflow.keras
import numpy as np
from tensorflow.keras.preprocessing import image


mlflow.set_tracking_uri("http://127.0.0.1:5000") 
run_id = "a23e98f2355c419f9eaa3a380f2bea2b"

model_uri = f"runs:/{run_id}/model"  # Modell elérési útvonal
model = mlflow.keras.load_model(model_uri)

model.summary()