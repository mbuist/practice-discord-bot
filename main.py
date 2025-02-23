import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv



class Client(commands.Bot):

    load_dotenv()

    # async def on_ready(self):
    #     print(f'Logged on as {self.user}!')

        # try:
        #     guild = discord.Object(id=1336012743920324739)
        #     synced = await self.tree.sync(guild=guild)
        #     print(f'Synced {len(synced)} commands to build {guild.id}')
        # except Exception as e:
        #     print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        # stop bot from replying to itself
        if (message.author == self.user):
            return
        if (message.content.lower().startswith('hello')):
            await message.channel.send(f'Hi there {message.author}')
        if (message.content.lower().startswith('bye')):
            await message.channel.send(f'Bye Bye! {message.author}')

    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        await reaction.message.channel.send(f'You reacted to "{reaction.message.content}"')


# on_ready()
# on_message(message)
# on_message_edit(before, after)
# on_message_delete(message)
# on_message_join(member)# on_member_remove(member)
# on_member_update(before, after)
# on_guild_join(guild)
# on_guild_remove(guild)
# on_reaction_remove(reaction, user)
# on_raw_message_delete(payload)
# on_command_error(ctx , error)


intents = discord.Intents.default()
intents.message_content = True
# we don't actually need the command prefix since they're outdated
client = Client(command_prefix="!", intents=intents)

# get secret stuff from environment varables
GUILD_ID = discord.Object(id=int(os.getenv('GUILD_ID')))
TOKEN = os.getenv('DISCORD_TOKEN')

@client.tree.command(name="hello", description="Say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("hi there!")

@client.tree.command(name="printer", description="I will print whatever you give me!", guild=GUILD_ID)
async def print(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)

# @client.tree.command(name="embed", description="embed demo", guild=GUILD_ID)
# async def embed(interaction: discord.Interaction):
#     embed = discord.Embed(tile="I am a title", description="i am description")
#     await interaction.response.send_message(embed=embed)

# client = Client(intents=intents)
client.run(TOKEN)