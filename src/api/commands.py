import requests
import pandas as pd
import pika

def post_data(data, queue_name, host = "localhost", port = 5672, user = "guest", password = "guest"):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=pika.PlainCredentials(user, password)))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='', routing_key=queue_name, body=data.encode('utf-8'))
    channel.close()
    connection.close()

if __name__ == "__main__":
    url = "http://localhost:8000"
    run_id = "041568b301a744b6b8a411e21d594107"
    resp = requests.get(url + "/model/" + run_id)    