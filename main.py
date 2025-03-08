import os
import discord
from discord.ext import commands
from discord import app_commands
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Dictionary of routes to stops
bus_routes = {
    "A": ["College Avenue Student Center", "The Yard", "Student Activities Center",
          "Stadium West Lot", "Hill Center (North)", "Science Buildings",
          "Busch Student Center", "Werblin Recreation Center"],
    "B": ["Livingston Student Center", "Quads", "Hill Center (North)",
          "Science Buildings", "Busch Student Center", "Livingston Plaza"],
    "C": ["Stadium West Lot", "Hill Center (North)", "Allison Road Classroom Building",
          "Hill Center (South)"],
    "EE": ["College Avenue Student Center", "The Yard", "SoCam Apartments (SB)",
           "Red Oak Lane", "Lipman Hall", "Biel Road", "Henderson Apartments",
           "Gibbons", "College Hall", "SoCam Apartments (NB)", "Student Activities Center"],
    "LX": ["College Avenue Student Center", "The Yard", "Student Activities Center",
           "Livingston Plaza", "Livingston Student Center", "Quads"],
    "REXB": ["Red Oak Lane", "Lipman Hall", "College Hall", "Hill Center (North)",
             "Allison Road Classroom Building", "Hill Center (South)"],
    "REXL": ["Red Oak Lane", "Lipman Hall", "College Hall", "Livingston Plaza",
             "Livingston Student Center"]
}

# Create bot instance with command prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Autocomplete function for bus routes
async def route_autocomplete(interaction: discord.Interaction, current: str):
    matches = [
        app_commands.Choice(name=route_name, value=route_name)
        for route_name in bus_routes
        if current.lower() in route_name.lower()
    ]
    return matches[:25]  # Discord allows max 25 suggestions

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"Logged in as {bot.user}. Slash commands synced!")
    except Exception as e:
        print("Error syncing commands:", e)

# Slash command to greet the user
@bot.tree.command(name="hello", description="Say hello to the bot!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}, I'm online! 🚀")

# Slash command to get Rutgers NB bus routes
@bot.tree.command(name="get_routes", description="Get the stops for a Rutgers NB bus route.")
@app_commands.describe(route="Select the bus route name")
@app_commands.autocomplete(route=route_autocomplete)
async def get_routes(interaction: discord.Interaction, route: str):
    stops = bus_routes.get(route)
    if not stops:
        await interaction.response.send_message(f"Could not find a route named **{route}**. Try again.", ephemeral=True)
        return

    route_title = f"**{route.upper()}** Bus Stops"
    stop_list = "\n".join(f"• {stop}" for stop in stops)
    await interaction.response.send_message(f"{route_title}\n{stop_list}")

# Slash command to get the dinner menu at Busch Dining Hall
@bot.tree.command(name="dinner_on_busch", description="Get today's dinner menu at Busch Dining Hall.")
async def dinner_on_busch(interaction: discord.Interaction):
    url = "https://menuportal23.dining.rutgers.edu/foodpronet/pickmenu.aspx?locationNum=04&locationName=Busch+Dining+Hall"
    
    response = requests.get(url)
    if response.status_code != 200:
        await interaction.response.send_message("Failed to retrieve the menu. Try again later.", ephemeral=True)
        return

    soup = BeautifulSoup(response.text, "html.parser")
    menu_items = []

    for item in soup.find_all("fieldset"):
        count = 0
        for foodItem in item:
            if count == 1:
                menu_items.append(foodItem.text.strip())
            count += 1

    if not menu_items:
        await interaction.response.send_message("Could not find any dinner items.", ephemeral=True)
        return

    menu_text = "**Busch Dining Hall Dinner Menu**\n" + "\n".join(f"• {item}" for item in menu_items)
    await interaction.response.send_message(menu_text[:2000])  # Discord limits messages to 2000 chars

# Run the bot
bot.run(TOKEN)
