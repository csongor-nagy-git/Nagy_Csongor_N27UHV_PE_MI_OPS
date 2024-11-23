import requests

if __name__ == "__main__":
    url = "http://localhost:8000"
    run_id = "c49025503fee4cb7b25669f8bc919b1e" # your mlflow run_id please
    resp = requests.get(url + "/model/" + run_id)    