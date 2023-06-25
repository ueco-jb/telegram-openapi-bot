#!/usr/bin/env python3
# pylint: disable=wrong-import-position

import yaml
import asyncio
import contextlib
import logging
import openai
from typing import NoReturn

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Bot
from telegram.error import Forbidden, NetworkError

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def read_config(filename):
    with open(filename, "r") as file:
        config = yaml.safe_load(file)
    return config


async def main() -> NoReturn:
    config = read_config("config.yaml")

    # Setting up OpenAI and Telegram bot with respective keys
    openai.api_key = config["openai-key"]
    telegram_key = config["telegram-key"]
    authorized_user = config["authorized-user"]

    """Run the bot."""
    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    async with Bot(telegram_key) as bot:
        # get the first pending update_id, this is so we can skip over it in case
        # we get a "Forbidden" exception.
        try:
            update_id = (await bot.get_updates())[0].update_id
        except IndexError:
            update_id = None

        logger.info("listening for new messages...")
        while True:
            try:
                update_id = await prompt(bot, update_id, authorized_user)
            except NetworkError:
                await asyncio.sleep(1)
            except Forbidden:
                # The user has removed or blocked the bot.
                update_id += 1


async def prompt(bot: Bot, update_id: int, authorized_user) -> int:
    """Send prompt through OpenAI API."""
    # Request updates after the last update_id
    updates = await bot.get_updates(offset=update_id, timeout=10)
    for update in updates:
        next_update_id = update.update_id + 1

        # check if the message is from the authorized user

        if update.message.from_user.id == authorized_user:
            # your bot can receive updates without messages
            # and not all messages contain text
            if update.message and update.message.text:
                # Generate a response using OpenAI GPT-3
                # response = openai.Completion.create(
                #     engine="text-davinci-002",
                #     prompt=update.message.text,
                #     max_tokens=60
                # )
                response = await asyncio.to_thread(
                    openai.ChatCompletion.create,
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": update.message.text},
                    ],
                )

                # Reply to the message
                logger.info("Found message %s!", update.message.text)
                await update.message.reply_text(
                    response["choices"][0]['message']['content']
                )
        return next_update_id
    return update_id


if __name__ == "__main__":
    with contextlib.suppress(
        KeyboardInterrupt
    ):  # Ignore exception when Ctrl-C is pressed
        asyncio.run(main())
