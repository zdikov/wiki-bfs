import concurrent.futures
import json
import pika
from concurrent import futures

from wiki_pb2_grpc import *
from wiki_pb2 import *

id_to_future = {}


class Wiki(WikiServicer):
    def __init__(self):
        self._count = 0

    def enqueue_request(self, url_from, url_to):
        req_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        req_channel = req_connection.channel()

        req_channel.queue_declare(queue='requests-queue')

        req_channel.basic_publish(exchange='', routing_key='requests-queue', body=json.dumps(
            {'url_from': url_from, 'url_to': url_to, 'id': self._count}).encode())

        req_connection.close()

    def FindShortestPath(self, request, context):
        self._count += 1

        self.enqueue_request(request.url_from, request.url_to)
        id_to_future[self._count] = concurrent.futures.Future()
        return ShortestPathResponse(id_to_future[self._count].result())


def callback(ch, method, properties, body):
    d = json.loads(body.decode())
    urls = d['urls']
    id_to_future[d['id']].set_result(urls)


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_WikiServicer_to_server(Wiki(), server)
    server.add_insecure_port('[::]:8080')
    server.start()

    resp_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    resp_channel = resp_connection.channel()
    resp_channel.queue_declare(queue='response-queue', durable=True)
    resp_channel.basic_consume(queue='response-queue', on_message_callback=callback)
    resp_channel.start_consuming()

    server.wait_for_termination()
