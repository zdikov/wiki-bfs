FROM python:3.8

RUN mkdir /root/app/
WORKDIR /root/app/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "-c", "while ! curl -s rabbitmq:15672 > /dev/null; do echo waiting for rabbitmq; sleep 3; done; python worker.py"]
