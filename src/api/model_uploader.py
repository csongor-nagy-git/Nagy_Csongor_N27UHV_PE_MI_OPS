import mlflow
import mlflow.tensorflow
import tensorflow as tf
import numpy as np

# Model betöltése .h5 formátumból
model = tf.keras.models.load_model('C:\\Users\\Csocsesz\\Downloads\\model.h5')

# Lokálisan futó MLFlow példány beállítása
mlflow.set_tracking_uri("http://localhost:5000")



# Modell feltöltése MLFlow-ba
with mlflow.start_run():
    mlflow.tensorflow.log_model(model, "model")