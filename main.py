from typing import List

import discord
from discord import app_commands
from dotenv import dotenv_values

import scraper

env_vars = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

classlist = scraper.get_class_list(update=True)

guildIDs = []

@client.event
async def on_ready():
    print(classlist)
    print(f'Logged on as {client.user}!')
    guildC = 0
    # Automatically check all joined guilds
    for guild in client.guilds:
        guildIDs.append(guild.id)
        print(f"joined to guild: {guild.id} (name: {guild.name})")
        guildC += 1
    
    i = 0;
    while (client.is_ws_ratelimited()):
        if (i % 50 == 0 or i == 0):
            print("rate limited D:")
            i += 1

    # Global sync for now
    # Guild specific sync broke everything >>.<< 
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
@tree.command(name="addclass", description="Add a class to your roles", guilds=guildIDs)
@app_commands.autocomplete(school=school_autocomplete)
# Add the guild ids in which the slash command will appear. If it should be in all, remove the argument,
# but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def add_class(interaction: discord.Interaction, school: str, class_id: str):
    class_full_name = school + " " + class_id
    class_full_name.upper() # Jank, but makes it case insensitive
    print(class_full_name)
    user = interaction.user
    print(check_valid(class_full_name))

    # if the role already exists, then give it to the user
    if discord.utils.get(interaction.guild.roles, name=class_full_name):
        # if they already have it then we don't really need to do anything...
        if discord.utils.get(user.guild.roles, name=class_full_name):
            await interaction.response.send_message("You already have this role.", ephemeral=True)
            return

        # assign the role
        await user.add_roles(discord.utils.get(user.guild.roles, name=class_full_name))
        await interaction.response.send_message("Done!", ephemeral=True)
        return

    # if it doesn't, then create the role and then add the user
    elif check_valid(class_full_name):
        print(class_full_name)
        print(user.guild.roles)
        role = await interaction.guild.create_role(name=class_full_name)
        await user.add_roles(role)
        await interaction.response.send_message("Done!", ephemeral=True)
        return

    # we really shouldn't be here but just in case...
    await interaction.response.send_message("Failed ;_;.", ephemeral=True)


# noinspection PyUnresolvedReferences
@tree.command(name="removeclass", description="Remove a class from your roles",
              guilds=guildIDs)
@app_commands.autocomplete(school=school_autocomplete)
async def remove_class(interaction: discord.Interaction, school: str, class_id: str):
    class_full_name = school + " " + class_id
    class_full_name.upper()

    if not check_valid(class_full_name):
        return

    user = interaction.user
    # if the role already exists, then remove it if they have it
    if discord.utils.get(interaction.guild.roles, name=class_full_name):
        role = discord.utils.get(interaction.guild.roles, name=class_full_name)
        if discord.utils.get(user.guild.roles, name=class_full_name):
            await user.remove_roles(role)
            await interaction.response.send_message("Done!", ephemeral=True)
            return

        await interaction.response.send_message("You don't have this role.", ephemeral=True)
        return

    await interaction.response.send_message("Failed ;_;.", ephemeral=True)


def check_valid(id: str):
    return id in classlist


client.run(env_vars["APPLICATION_KEY"])
