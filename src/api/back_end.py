from fastapi import FastAPI
import mlflow
import mlflow.pyfunc

model = None
signature = None
app = FastAPI()

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