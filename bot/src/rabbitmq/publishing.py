import pika

from utils import logging
from utils.config import props

LOGGER = logging.get_logger()

RMQ_PORT = props["RABBIT_MQ"]["RMQ_PORT"]
RMQ_HOST = props["RABBIT_MQ"]["RMQ_HOST"]
RMQ_HEARTBEAT_INTERVAL = props.getint("RABBIT_MQ", "RMQ_HEARTBEAT_INTERVAL")
RMQ_INPUT_QUEUE = props["RABBIT_MQ"]["RMQ_INPUT_QUEUE_NAME"]
RMQ_OUTPUT_QUEUE = props["RABBIT_MQ"]["RMQ_OUTPUT_QUEUE_NAME"]
RMQ_EXCHANGE_QUEUE = props["RABBIT_MQ"]["RMQ_EXCHANGE_NAME"]
RMQ_USER = props.get("RABBIT_MQ", "RMQ_USERNAME")
RMQ_PASSWORD = props.get("RABBIT_MQ", "RMQ_PASSWORD")


def init_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost", port=5672))
    channel = connection.channel()
    channel.queue_declare(queue=RMQ_INPUT_QUEUE)
    return connection, channel
