# autobot

Autoware Discord technical support bot

## Installation

```bash
pip install openai \
discord.py

sudo apt install libffi-dev libnacl-dev python3-dev
```

## Usage

### Get the `guild_id` and `channel_id`

- Open up the discord in a browser.
- Go to the channel you want to use the bot in.
  - The channel should be a Forum channel.
  - Make sure the channel is selected, not a thread.
- The URL in the browser will be in the following format:
  - "https://discord.com/channels/{guild_id}/{channel_id}"

### Run the bot

```console
$ python3 main.py --help
usage: main.py [-h] guild_id channel_id token_bot api_key_openai assistant_id

Run Autobot with specified parameters.

positional arguments:
  guild_id        The ID of the guild
  channel_id      The ID of the channel
  token_bot       The bot token
  api_key_openai  OpenAI API key
  assistant_id    OpenAI Assistant ID

options:
  -h, --help      show this help message and exit
```

Example:

```bash
python3 main.py 123456789012345678 1234567890123456789 Str1.Str2.Str3 sk-Str4 asst_Str5
```