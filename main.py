from typing import List

import discord
from discord import app_commands
from dotenv import dotenv_values

import scraper

print("main.py starting!")
env_vars = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True

print("grabbing client and tree")
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

print("grabbing values")
classlist = scraper.get_class_list(update=True)


@client.event
async def on_ready():
    print(classlist)
    print(f'Logged on as {client.user}!')
    await tree.sync()
    print("Ready!")


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
# Add the guild ids in which the slash command will appear. If it should be in all, remove the argument,
# but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def add_class(interaction: discord.Interaction, school: str, class_id: str):
    class_full_name = (school + " " + class_id).upper()
    print(class_full_name)
    user = interaction.user
    print(check_valid(class_full_name))

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
    print(class_full_name)
    print(user.roles)
    role = await interaction.guild.create_role(name=class_full_name)
    await user.add_roles(role)
    await interaction.response.send_message("Done!", ephemeral=True)
    return


# noinspection PyUnresolvedReferences
@tree.command(name="removeclass", description="Remove a class from your roles")
@app_commands.autocomplete(school=school_autocomplete)
async def remove_class(interaction: discord.Interaction, school: str, class_id: str):
    class_full_name = (school + " " + class_id).upper()

    if not check_valid(class_full_name):
        await interaction.response.send_message("Please enter a valid class", ephemeral=True)
        return

    user = interaction.user
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


@tree.command(name="bonk", description="...bonk!")
async def bonk(interaction: discord.Interaction, user: discord.Member):
    e = discord.Embed(
        description=(interaction.user.mention + " bonked " + user.mention))
    e.set_image(url="https://media.tenor.com/zdcbh9URQCsAAAAd/bonk-doge.gif")
    await interaction.response.send_message(embed=e)


def check_valid(id: str):
    return id in classlist

print("starting bot!")
client.run(env_vars["APPLICATION_KEY"])
