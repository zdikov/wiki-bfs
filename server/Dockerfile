FROM python:3.8

RUN mkdir /root/app/
WORKDIR /root/app/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY wiki.proto .
RUN python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. wiki.proto

COPY . .

CMD ["bash", "-c", "while ! curl -s rabbitmq:15672 > /dev/null; do echo waiting for rabbitmq; sleep 3; done; python server.py"]
