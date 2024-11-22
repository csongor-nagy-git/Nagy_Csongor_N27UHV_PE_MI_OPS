
from fastapi import FastAPI, Request, BackgroundTasks
import mlflow


app = FastAPI()

@app.get("/") 
async def read_root():
    """Default path. See /docs for more."""
    return "Hello World"
    ## TODO:


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("back_end:app", host="localhost", port=8000, reload=True)