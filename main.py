import discord
from discord import app_commands

from dotenv import dotenv_values

import scraper

env_vars = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

classlist = scraper.get_class_list(update=False)


@client.event
async def on_ready():
    print(classlist)
    print(f'Logged on as {client.user}!')
    await tree.sync(guild=discord.Object(id=env_vars["TEST_GUILD_ID"]))
    print("Ready!")


# https://stackoverflow.com/questions/71165431/how-do-i-make-a-working-slash-command-in-discord-py
@tree.command(name="addclass", description="add a role for a class", guild=discord.Object(id=env_vars["TEST_GUILD_ID"]))
# Add the guild ids in which the slash command will appear. If it should be in all, remove the argument,
# but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def add_class(interaction: discord.Interaction, id: str):
    print(id)
    user = interaction.user

    print(check_valid(id))

    # if the role already exists, then give it to the user
    if discord.utils.get(interaction.guild.roles, name=id):
        # if they already have it then we don't really need to do anything...
        if discord.utils.get(user.guild.roles, name=id):
            await interaction.response.send_message("You already have this role. ")
            return

        # assign the role
        await user.add_roles(discord.utils.get(user.guild.roles, name=id))
        await interaction.response.send_message("Done! ")
        return

    # if it doesn't, then create the role and then add the user
    elif check_valid(id):
        print(id)
        print(user.guild.roles)
        role = await interaction.guild.create_role(name=id)
        await user.add_roles(role)
        await interaction.response.send_message("Done! ")
        return

    # we really shouldn't be here but just in case...
    await interaction.response.send_message("Failed ;_;. ")


@tree.command(name="removeclass", description="remove a role for a class", guild=discord.Object(id=env_vars["TEST_GUILD_ID"]))
async def remove_class(interaction: discord.Interaction, id: str):
    user = interaction.user
    # if the role already exists, then give it to the user
    if discord.utils.get(interaction.guild.roles, name=id):
        # if they already have it then we don't really need to do anything...
        role = discord.utils.get(interaction.guild.roles, name=id)
        if discord.utils.get(user.guild.roles, name=id):
            await user.remove_roles(role)
            await interaction.response.send_message("Done! ")
            return

        await interaction.response.send_message("You don't have this role. ")
        return

    await interaction.response.send_message("Failed ;_;. ")


def check_valid(id: str):
    return id in classlist


client.run(env_vars["APPLICATION_KEY"])
