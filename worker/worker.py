import json
import pika
from bfs import find_shortest_path


def enqueue_response(req_id, urls):
    resp_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    resp_channel = resp_connection.channel()

    resp_channel.queue_declare(queue='response-queue')

    resp_channel.basic_publish(exchange='', routing_key='response-queue', body=json.dumps(
        {'urls': urls, 'id': req_id}).encode())

    resp_connection.close()


def callback(ch, method, properties, body):
    d = json.loads(body.decode())
    req_id = d['id']
    url_from = d['url_from']
    url_to = d['url_to']

    urls = find_shortest_path(url_from, url_to)
    enqueue_response(req_id, urls)


req_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
req_channel = req_connection.channel()
req_channel.queue_declare(queue='request-queue', durable=True)
req_channel.basic_consume(queue='request-queue', on_message_callback=callback)
req_channel.start_consuming()
