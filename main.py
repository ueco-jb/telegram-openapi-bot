#!/usr/bin/env python3

import yaml
from telegram import Bot
from openai import OpenAI

def read_config(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Ask me anything!')

def respond(update: Update, context: CallbackContext) -> None:
    """Respond to the user's message."""
    message = update.message.text
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=message,
      max_tokens=60
    )
    update.message.reply_text(response.choices[0].text.strip())

def main():
    config = read_config('config.yaml')

    # Setting up OpenAI and Telegram bot with respective keys
    openai_key = config['openai-key']
    telegram_key = config['telegram-key']

    """Start the bot."""
    updater = Updater(token=telegram_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
