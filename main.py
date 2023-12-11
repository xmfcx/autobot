from discord_server_custom import run_autobot
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Autobot with specified parameters.")
    parser.add_argument("guild_id", type=int, help="The ID of the guild")
    parser.add_argument("channel_id", type=int, help="The ID of the channel")
    parser.add_argument("token_bot", type=str, help="The bot token")
    parser.add_argument("api_key_openai", type=str, help="OpenAI API key")
    parser.add_argument("assistant_id", type=str, help="OpenAI Assistant ID")

    args = parser.parse_args()

    print(f"Running bot with:")
    print(f"guild_id={args.guild_id}")
    print(f"channel_id={args.channel_id}")
    print(f"token_bot={args.token_bot}")
    print(f"api_key_openai={args.api_key_openai}")
    print(f"assistant_id={args.assistant_id}")

    run_autobot(args.guild_id, args.channel_id, args.token_bot, args.api_key_openai, args.assistant_id)
