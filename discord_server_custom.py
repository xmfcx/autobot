import functools
import typing
import discord


def run_autobot(guild_id: int, channel_id: int, token_bot: str, api_key_openai: str, assistant_id: str):
    intents = discord.Intents.all()
    intents.message_content = True

    client_discord = discord.Client(intents=intents)
    tree = discord.app_commands.CommandTree(client_discord)

    guild_bot = discord.Object(id=guild_id)

    @client_discord.event
    async def on_ready():
        tree.copy_global_to(guild=guild_bot)
        await tree.sync(guild=guild_bot)
        # print "ready" in the console when the bot is ready to work
        print("The bot is ready!")

    async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
        """Runs a blocking function in a non-blocking way"""
        func = functools.partial(blocking_func, *args,
                                 **kwargs)  # `run_in_executor` doesn't support kwargs, `functools.partial` does
        return await client_discord.loop.run_in_executor(None, func)

    @tree.command(name="autobot")
    async def autobot(interaction: discord.Interaction):
        print(f"channel_id: {interaction.channel_id}")
        print(f"interaction.channel.type: {interaction.channel.type}")

        channel_is_right = False
        if interaction.channel.type == discord.ChannelType.public_thread:
            if interaction.channel.parent_id == channel_id:
                channel_is_right = True

        if not channel_is_right:
            channel_bot_testing = await client_discord.fetch_channel(channel_id)
            await interaction.response.send_message(f"Please use the {channel_bot_testing.mention} channel.")
            return

        # allowed_role = "autobot-allowed"
        # role_is_right = False
        # for role in interaction.user.roles:
        #     if role.name == "autobot-allowed":
        #         role_is_right = True
        #         break
        #
        # if not role_is_right:
        #     await interaction.response.send_message(
        #         f"Only the people with the `{allowed_role}` role can call Autobot.")
        #     return

        await interaction.response.send_message(f'Let me help!')

        current_channel = await client_discord.fetch_channel(interaction.channel_id)

        last_x_messages = []
        async for msg in current_channel.history(limit=100):
            last_x_messages.append(msg)

        last_x_messages.reverse()
        msgs_history = []
        from autobot_gpt import form_msg_user
        msgs_history.append(form_msg_user("title", current_channel.name))
        for msg in last_x_messages:
            print(f"msg.author.display_name: {msg.author}")
            print(f"client_discord.user: {client_discord.user}")

            # from autobot_gpt import form_msg_bot
            # if msg.author == client_discord.user:
            #     msgs_history.append(form_msg_bot(msg.content))
            # else:
            #     msgs_history.append(form_msg_user(msg.author.display_name, msg.content))
            msg_actual_content = msg.content
            if msg.embeds and len(msg.embeds) > 0:
                for embed in msg.embeds:
                    # if embed.title:
                    #     msg_actual_content += "\n" + msg.embeds[0].title
                    if embed.description:
                        msg_actual_content += "\n" + msg.embeds[0].description
            msgs_history.append(form_msg_user(msg.author.display_name, msg_actual_content))

        # remove the last message from the history
        msgs_history.pop()

        print(f"message history:")
        for msg in msgs_history:
            print(f"msg: {msg}")

        from autobot_gpt import run_assistant

        msg_assistant = await run_blocking(run_assistant, api_key_openai=api_key_openai, assistant_id=assistant_id,
                                           messages=msgs_history)

        em = discord.Embed(title=f"Response", description=f"{msg_assistant}")
        await current_channel.send(embed=em)

    client_discord.run(token_bot)
