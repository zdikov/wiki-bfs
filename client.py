import copy

import google.protobuf.empty_pb2
import google.protobuf.json_format

from wiki_pb2_grpc import *
from wiki_pb2 import *

if __name__ == '__main__':
    while True:
        address = input('Enter server address:port --> ')
        if not address:
            address = '127.0.0.1:8080'
        urls = input('Enter links to english wiki pages --> ').split()
        if len(urls) != 2:
            print('Wrong number of links, try again')
            continue
        url_from, url_to = urls
        if '/wiki/' not in url_from or '/wiki/' not in url_to:
            print('Links must contain "/wiki/", try again')
            continue

        url_from = url_from[url_from.find('/wiki/'):]
        url_to = url_to[url_from.find('/wiki/'):]

        with grpc.insecure_channel(address) as channel:
            stub = WikiStub(channel)
            resp = stub.FindShortestPath(ShortestPathRequest(url_from=url_from, url_to=url_to))
            for url in resp.urls:
                print('https://en.wikipedia.org' + url)
