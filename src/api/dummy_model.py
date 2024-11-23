import mlflow
import mlflow.pyfunc
import numpy as np
from PIL import Image

# Define a dummy model class
class DummyImageModel(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input):
        # Dummy prediction: Randomly generates a softmax output for each image
        num_samples = model_input.shape[0]
        
        # Random logits for 5 classes
        logits = np.random.randn(num_samples, 5)
        
        # Apply softmax to logits
        exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))  # Stability fix
        softmax_output = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
        
        return softmax_output

# Function to preprocess an image (resize to 224x224, normalize to 0-1 range)
def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))  # Resize to 224x224
    img_array = np.array(img) / 255.0  # Normalize pixel values
    return img_array

# Set the MLflow tracking URI
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Set experiment name
mlflow.set_experiment("ImageDummyModelExperiment")

# Log the dummy model
with mlflow.start_run(run_name="ImageDummyModelRun"):
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=DummyImageModel(),
        registered_model_name="ImageDummyModel"
    )
    print("Model logged successfully.")
