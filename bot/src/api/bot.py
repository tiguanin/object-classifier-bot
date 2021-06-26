import logging
import traceback
import uuid

import pika
from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

import rabbitmq.publishing
from utils.config import props


class TelegramBot:
    TOKEN = props["TELEGRAM_BOT"]["TOKEN"]
    INPUT_PATH = props["PATHS"]["SRC_RAW_STORAGE"]
    RMQ_INPUT_QUEUE = props["RABBIT_MQ"]["RMQ_INPUT_QUEUE_NAME"]
    connection = None
    channel = None
    LOGGER = logging.getLogger(__name__)

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    def init_rabbitmq_connection(self, update: Update, context: CallbackContext):
        user = update.effective_user
        self.connection, self.channel = rabbitmq.publishing.init_rabbitmq_connection()
        update.message.reply_markdown_v2(
            fr"Hi {user.mention_markdown_v2()}\! Service was started ❤",
            reply_markup=ForceReply(selective=True),
        )

    def help_command(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text("It's simple. No help needed.")

    def stop_rabbitmq_connection(
        self, update: Update, context: CallbackContext
    ) -> None:
        try:
            self.channel.close()
            self.connection.close()
        except KeyboardInterrupt:
            self.LOGGER.info("Connection closed manually by user")
            self.channel.stop_consuming()
            self.connection.close()
        except pika.exceptions.ConnectionClosedByBroker:
            self.LOGGER.error("Connection closed by broker. Recovering again...")
            traceback.print_exc()
        finally:
            update.message.reply_text("💔 Connection closed.")

    def classify_image(self, update: Update, context: CallbackContext) -> None:
        file = update.message.photo[-1].get_file()
        path = file.download(custom_path=self.INPUT_PATH + str(uuid.uuid4()) + ".jpg")
        self.channel.basic_publish(
            exchange="", routing_key=self.RMQ_INPUT_QUEUE, body=path
        )

    def start_bot(self) -> None:
        updater = Updater(self.TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", self.init_rabbitmq_connection))
        dispatcher.add_handler(CommandHandler("help", self.help_command))
        dispatcher.add_handler(CommandHandler("stop", self.stop_rabbitmq_connection))
        dispatcher.add_handler(MessageHandler(Filters.photo, self.classify_image))

        updater.start_polling()
        updater.idle()
