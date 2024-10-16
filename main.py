from functools import partial

import telebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
from db.queries import SubscriberQueryRepo

bot = telebot.TeleBot(token=config.TELEGRAM_BOT_TOKEN)

engine = create_engine(config.url, echo=True)  # echo=True - shows SQL in the console
session_pool = sessionmaker(bind=engine)


@bot.message_handler(commands=["start", ])
def start_handler(message):
    """Handle start requests from the bot."""
    telegram_id = message.from_user.id
    chat_id = message.chat.id

    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    full_name = f"{first_name} {last_name or ''}" if first_name or last_name else username

    send_message = partial(bot.send_message, chat_id=chat_id, parse_mode="html")

    with session_pool() as session:
        query_repo = SubscriberQueryRepo(session=session)
        subscriber = query_repo.get_subscriber(telegram_id=telegram_id)
        if subscriber:
            send_message(text=config.SUBSCRIBER_ALREADY_EXIST_MSG.format(user_name=full_name))
        else:
            query_repo.create_subscriber(telegram_id=telegram_id, first_name=first_name, last_name=last_name)
            send_message(text=config.SUCCESSFUL_SUBSCRIPTION_MSG.format(user_name=full_name))


if __name__ == "__main__":
    bot.infinity_polling()
