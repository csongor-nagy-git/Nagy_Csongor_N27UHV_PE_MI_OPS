import mlflow
import mlflow.keras
import json

# 1. MLflow Tracking URI beállítása
mlflow.set_tracking_uri("file:///C:/Users/Csocsesz/Desktop/PE_MI_Szakdoga/Mappa/Nagy_Csongor_N27UHV_PE_MI_OPS/mlruns")  # Helyi MLflow szerver vagy URL

# 2. Modell és metrikák fájlnevei
model_path = "C:/Users/Csocsesz/Downloads/my_model/1st run/"  # TensorFlow SavedModel mappa elérési útja
# model_path = "path_to_saved_model/model.h5"  # Modell elérési útja
metrics_path = "C:/Users/Csocsesz/Downloads/metrics.json"  # Metrikák elérési útja

# 3. Betöltés
print("Loading model...")
model = mlflow.keras.load_model(model_path)

print("Loading metrics...")
with open(metrics_path, "r") as f:
    metrics = json.load(f)

# 4. MLflow futás indítása
with mlflow.start_run() as run:
    # Modell regisztrálása
    print("Logging model...")
    mlflow.keras.log_model(keras_model=model, artifact_path="model", registered_model_name="my_model_name")
    
    # Metrikák regisztrálása
    print("Logging metrics...")
    for metric_name, metric_value in metrics.items():
        mlflow.log_metric(metric_name, metric_value)

    # Paraméterek opcionálisan hozzáadhatók
    mlflow.log_param("description", "Model uploaded from TPU training session.")

    # Run ID kiíratása
    print(f"Run ID: {run.info.run_id}")