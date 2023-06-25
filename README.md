# Telegram OpenAI Bot

This is a simple Telegram bot that uses the OpenAI API to generate responses to user messages. It is designed to respond only to messages from a specific authorized user.

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/ueco-jb/telegram-openapi-bot.git
    cd telegram-openapi-bot
    ```

2. Create a virtual environment and install the dependencies:

    ```
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

## Configuration

You need to set up two API keys: one for Telegram, and one for OpenAI.

1. **Telegram Bot Token**: Follow the instructions on [BotFather](https://core.telegram.org/bots#botfather) to create a new Telegram bot and get your bot token.

2. **OpenAI API Key**: Sign up on [OpenAI](https://beta.openai.com/signup/) to get your API key.

3. **Telegram user ID**: In order to restrict bot to only one user, enter telegram user ID. To obtain your Telegram ID, you can start a chat with the `@get_id_bot` on Telegram, click on the START button at the bottom, and the bot will then send you a message containing your user ID.

Once you have your API keys, enter the values in `config.yaml` file.

## Running the Bot

With your virtual environment activated and the `config.yaml` file filled with your API keys, you can run the bot with:
```
python3 main.py
```

The bot will now listen for new messages from the authorized user and respond to them using the OpenAI API.


