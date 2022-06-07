import nextcord
from nextcord.ext import commands
import os

intents = nextcord.Intents().all()

client = commands.Bot(command_prefix='*', intents=intents, help_command=None)


def custom_id(view: str, id: int):
    return f"{view}:{id}"


client.load_extension('map_banning')
client.load_extension('db_settings')
client.load_extension('db_operations')


@client.event
async def on_ready():
    """ Event handler that is called when bot is turned on. """
    print("Bot is ready")
    await client.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.watching,
            name="małe mapy"
        )
    )


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, nextcord.ext.application_checks.errors.ApplicationMissingPermissions):
        await ctx.send(f'You don\'t have {error.missing_permissions} permission to use this command.', delete_after=5)

client.run(os.getenv('TOKEN'))
