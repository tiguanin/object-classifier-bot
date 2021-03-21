import traceback

import pika
from pika import exceptions

from service.classifier import EfficientClassifier
from utils import logging
from utils.config import props

LOGGER = logging.get_logger()

RMQ_PORT = props['RABBIT_MQ']['RMQ_PORT']
RMQ_HOST = props['RABBIT_MQ']['RMQ_HOST']
RMQ_HEARTBEAT_INTERVAL = props.getint('RABBIT_MQ', 'RMQ_HEARTBEAT_INTERVAL')
RMQ_INPUT_QUEUE = props['RABBIT_MQ']['RMQ_INPUT_QUEUE_NAME']
RMQ_OUTPUT_QUEUE = props['RABBIT_MQ']['RMQ_OUTPUT_QUEUE_NAME']
RMQ_EXCHANGE_QUEUE = props['RABBIT_MQ']['RMQ_EXCHANGE_NAME']
RMQ_USER = props.get('RABBIT_MQ', 'RMQ_USERNAME')
RMQ_PASSWORD = props.get('RABBIT_MQ', 'RMQ_PASSWORD')

CLASSIFIER = EfficientClassifier()


def consume():
    credentials = pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD)
    parameters = pika.ConnectionParameters(host=RMQ_HOST, port=RMQ_PORT, heartbeat=RMQ_HEARTBEAT_INTERVAL,
                                           credentials=credentials, socket_timeout=15)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=RMQ_INPUT_QUEUE)
    channel.queue_declare(queue=RMQ_OUTPUT_QUEUE)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RMQ_INPUT_QUEUE, on_message_callback=on_message, auto_ack=True)
    LOGGER.info(' [*] Waiting for messages')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        LOGGER.info('Connection closed manually by user')
        channel.stop_consuming()
        connection.close()
    except pika.exceptions.ConnectionClosedByBroker:
        LOGGER.error('Connection closed by broker. Recovering again...')
        traceback.print_exc()
    finally:
        _close_connection(connection, channel)


def on_message(channel, method_frame, properties, body):
    LOGGER.info("get input image {}".format(body))
    try:
        image_path = body
        predicts_json = CLASSIFIER.predict(image_path)
        channel.basic_publish(exchange=RMQ_EXCHANGE_QUEUE,
                              routing_key=RMQ_OUTPUT_QUEUE,
                              body=predicts_json,
                              properties=pika.BasicProperties(content_type='application/json'))
        LOGGER.info('Message publish was confirmed')

    except Exception as e:
        LOGGER.error("error during process {}, error: {}".format(body, traceback.format_exc()))


def _close_connection(connection, channel):
    channel.stop_consuming()
    connection.close()
    LOGGER.info('Connection closed')
    consume()
