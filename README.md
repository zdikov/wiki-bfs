## Как запустить сервер:
```
docker-compose up --build --scale worker=2 rabbitmq worker server
```

## Как запустить клиент:
```
pip3 install -r server/requirements.txt
python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. server/wiki.proto
python3 client.py
```



