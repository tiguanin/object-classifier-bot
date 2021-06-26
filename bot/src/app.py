from api.bot import TelegramBot
import atexit


def exit_handler(telegram_bot: TelegramBot):
    telegram_bot.stop_rabbitmq_connection()


if __name__ == "__main__":
    bot = TelegramBot()
    bot.start_bot()
    atexit.register(exit_handler(bot))
    atexit.unregister(exit_handler(bot))
