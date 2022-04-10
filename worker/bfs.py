import requests
import re
from queue import SimpleQueue
from bs4 import BeautifulSoup

forbidden_patterns = [
    ':',  # Category:, Special:, Talk:, etc.
    '#',
    '.jpg',
    '.png',
]


def find_adjacent(url):
    page = requests.get('https://en.wikipedia.org' + url)
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find_all('a', href=re.compile(r'^/wiki/'))

    urls = []
    for element in elements:
        for pattern in forbidden_patterns:
            if pattern in element['href']:
                break
        else:
            urls.append(element['href'])

    return urls


def make_result(url_from, url_to, prev):
    result = []
    cur = url_to
    while cur != url_from:
        result.append(cur)
        cur = prev[cur]
    result.append(url_from)
    return reversed(result)


def find_shortest_path(url_from, url_to):
    queue = SimpleQueue()
    queue.put(url_from)
    visited = set(url_from)
    prev = {}
    while not queue.empty():
        cur = queue.get()
        for node in find_adjacent(cur):
            if node not in visited:
                visited.add(node)
                prev[node] = cur
                queue.put(node)
                if node == url_to:
                    return make_result(url_from, url_to, prev)
    return []


if __name__ == '__main__':
    url_from, url_to = input().split()
    url_from = url_from[url_from.find('/wiki/'):]
    url_to = url_to[url_to.find('/wiki/'):]
    print(url_from, '-->', url_to)
    result = find_shortest_path(url_from, url_to)
    for url in result:
        print('https://en.wikipedia.org' + url)
