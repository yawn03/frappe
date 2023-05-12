from typing import List

import discord
from discord import app_commands
from dotenv import dotenv_values
import random

import scraper

print("main.py starting!")
env_vars = dotenv_values(".env")

# setup intents
intents = discord.Intents.default()
intents.message_content = True

# Open connection with discord and grab our command tree
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Scrape classes
classlist: list = scraper.get_class_list(update=True)


@client.event
async def on_ready():
    print(classlist)
    print(f'Logged on as {client.user}!')

    # sync our commands globally
    await tree.sync()
    print("Ready!")


# Autocomplete decorator for school departments
async def school_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
    schools = ['ECE', 'M']
    return [
        app_commands.Choice(name=school, value=school)
        for school in schools if current.lower() in school.lower()
    ]


# https://stackoverflow.com/questions/71165431/how-do-i-make-a-working-slash-command-in-discord-py
# noinspection PyUnresolvedReferences
@tree.command(name="addclass", description="Add a class to your roles")
@app_commands.autocomplete(school=school_autocomplete)
async def add_class(interaction: discord.Interaction, school: str, class_id: str):
    # make a case-insensitive concat of the department and course number
    class_full_name = (school + " " + class_id).upper()

    user = interaction.user

    # Check for validity of the course, if not then quit
    if not check_valid(class_full_name):
        await interaction.response.send_message("Please enter a valid class", ephemeral=True)
        return

    # if the role already exists, then give it to the user
    if discord.utils.get(interaction.guild.roles, name=class_full_name):
        # if they already have it then we don't really need to do anything...
        if discord.utils.get(user.roles, name=class_full_name):
            await interaction.response.send_message("You already have this role.", ephemeral=True)
            return

        # assign the role
        await user.add_roles(discord.utils.get(user.guild.roles, name=class_full_name))
        await interaction.response.send_message("Done!", ephemeral=True)
        return

    # if it doesn't, then create the role and then add the user
    role = await interaction.guild.create_role(name=class_full_name)
    await user.add_roles(role)
    await interaction.response.send_message("Done!", ephemeral=True)
    return


# noinspection PyUnresolvedReferences
@tree.command(name="removeclass", description="Remove a class from your roles")
@app_commands.autocomplete(school=school_autocomplete)
async def remove_class(interaction: discord.Interaction, school: str, class_id: str):
    # make a case-insensitive concat of the department and course number
    class_full_name = (school + " " + class_id).upper()

    user = interaction.user

    # Check for validity of the course, if not then quit
    if not check_valid(class_full_name):
        await interaction.response.send_message("Please enter a valid class", ephemeral=True)
        return

    # if the role already exists, then remove it if they have it
    if discord.utils.get(interaction.guild.roles, name=class_full_name):
        role = discord.utils.get(interaction.guild.roles, name=class_full_name)
        if discord.utils.get(user.roles, name=class_full_name):
            await user.remove_roles(role)
            await interaction.response.send_message("Done!", ephemeral=True)
            return

        await interaction.response.send_message("You don't have this role.", ephemeral=True)
        return

    await interaction.response.send_message("Failed ;_;.", ephemeral=True)

def randBonk():
    return ['https://media.tenor.com/zdcbh9URQCsAAAAd/bonk-doge.gif',
            'https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWQ0Nzk1NDFkYTBmNTZiODdlNmQ4YmZjNmQxODhhYTFkNTIxNTQ2NyZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/6d7YORJ4gNKJZ6eE4o/giphy-downsized-large.gif',
            'https://media.tenor.com/Tg9jEwKCZVoAAAAd/bonk-mega-bonk.gif'][0 if random.randint(1, 100) > 25 else random.randint(1, 2)]

@tree.command(name="bonk", description="...bonk!")
async def bonk(interaction: discord.Interaction, user: discord.Member):
    e = discord.Embed()
    e.set_image(url=randBonk())
    await interaction.response.send_message(interaction.user.mention + " bonked " + user.mention, embed=e)


@tree.command(name="donk", description="...bonk!")
async def donk(interaction: discord.Interaction):
    await interaction.response.send_message("donk!")

def check_valid(id: str):
    return id in classlist


print("starting bot!")
client.run(env_vars["APPLICATION_KEY"])
