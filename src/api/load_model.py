import mlflow
import mlflow.keras
import numpy as np
import mlflow.pyfunc

mlflow.set_tracking_uri("http://127.0.0.1:5000") 
run_id = "a23e98f2355c419f9eaa3a380f2bea2b"

model_uri = f"runs:/{run_id}/model"  # Modell elérési útvonal
model = mlflow.pyfunc.load_model(model_uri)

# Make predictions with the loaded model
input_data = np.zeros((1, 224, 224, 3))  # Example input (10 dummy samples)
predictions = model.predict(input_data)
predicted_class = np.argmax(predictions, axis=1)
print("Predictions:", predictions)
print("Predicted class:", predicted_class)