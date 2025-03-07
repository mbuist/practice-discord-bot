import os
import discord
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up bot with command prefix
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        print(f'Connected to server: {guild.name} (ID: {guild.id})')
        
        # Find the first text channel where the bot can send messages
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(f'Hello! {bot.user} is now online! 🚀')
                break

@bot.command()
async def hey(ctx):
    await ctx.send("heyyyyyyyy")

@bot.command()
async def status(ctx):
    await ctx.send("good\nand what about u")

@bot.command()
async def dinner(ctx, campus: str):
    """Fetches dinner menu for the specified Rutgers campus (Busch, Livingston, College Ave, Cook)."""
    campus_urls = {
        "busch": "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=04&locationName=Busch+Dining+Hall",
        "livingston": "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=03&locationName=Livingston+Dining+Hall",
        "college": "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=01&locationName=Brower+Commons",
        "cook": "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=02&locationName=Neilson+Dining+Hall"
    }
    
    campus = campus.lower()
    if campus not in campus_urls:
        await ctx.send("Invalid campus name! Choose from: Busch, Livingston, College, Cook.")
        return
    
    today = datetime.today().strftime("%m/%d/%Y")
    url = f"{campus_urls[campus]}&dtdate={today}&activeMeal=Dinner"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        menu_items = []
        
        for item in soup.find_all("fieldset"):
            count = 0
            for foodItem in item:
                if count == 1:
                    menu_items.append(foodItem.text.strip())
                count += 1
        
        if menu_items:
            message = f"Dinner menu for {campus.capitalize()}:\n" + "\n".join(menu_items)
            for i in range(0, len(message), 1999):
                await ctx.send(message[i:i+1999])
        else:
            await ctx.send(f"No menu found for {campus.capitalize()} today.")
    else:
        await ctx.send(f"Failed to retrieve the menu. Error {response.status_code}")

bot.run(TOKEN)