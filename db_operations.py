import nextcord
from nextcord.ext import commands, application_checks
from db_settings import DatabaseSettings


class MapManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name='set_bot_channel', guild_ids=[955933461959569418, 926435401483309066, 218510314835148802])
    async def set_bot_channel(self, interaction: nextcord.Interaction):
        collection = await DatabaseSettings.db_connection('Mapiez_Database', 'Channels', interaction=interaction)
        if collection is None:
            return

        check = collection.find_one({'guild_id': interaction.guild_id})
        if check is None:
            collection.insert_one({'guild_id': interaction.guild_id, 'channel_id': interaction.channel_id})
        else:
            collection.update_one({'guild_id': interaction.guild_id},
                                  {'$set': {'channel_id': interaction.channel_id}})
        await interaction.response.send_message(f'Channel {interaction.channel.mention} was set for Mapież!')

    @nextcord.slash_command(name='add_map', guild_ids=[218510314835148802])
    async def add_map(self, interaction: nextcord.Interaction, game_name: str, map_name: str, map_emoji: str):
        """
        Command used to check player's rank and display information about it

            Args:
                interaction (nextcord.Interaction): Context of the command
                game_name (str): Name of the game that You want to add map for
                map_name (str): Name of the map that You want to add to the database
                map_emoji (str): Discord Emoji of the map that You want to add

            Returns:
                None
        """
        collection = await DatabaseSettings.db_connection('Mapiez_Database', 'Maps', interaction=interaction)

        if collection is None:
            return

        map_in_database = collection.find_one({'game_name': game_name, 'map_name': map_name})
        if map_in_database:
            await interaction.response.send_message(f'Map {map_emoji} **{map_name}**'
                                                    f' in {game_name} game is already in the database')
        else:
            collection.insert_one({
                'game_name': game_name,
                'map_name': map_name,
                'map_emoji': map_emoji,
                'times_banned': 0,
                'times_played': 0
            })
            await interaction.response.send_message(f'Map {map_emoji} **{map_name}**'
                                                    f' in **{game_name}** game has been added to the database')

    @nextcord.slash_command(name='remove_map', guild_ids=[218510314835148802])
    async def remove_map(self, interaction: nextcord.Interaction, game_name: str, map_name: str):
        """
        Command used to check player's rank and display information about it

            Args:
                interaction (nextcord.Interaction): Context of the command
                game_name (str): Name of the game that You want to remove map from
                map_name (str): Name of the map that You want to remove from database

            Returns:
                None
        """
        collection = await DatabaseSettings.db_connection('Mapiez_Database', 'Maps', interaction=interaction)

        if collection is None:
            return

        map_in_database = collection.find_one({'game_name': game_name, 'map_name': map_name})

        if map_in_database:
            collection.delete_one({
                'game_name': game_name,
                'map_name': map_name
            })
            await interaction.response.send_message(f'Map **{map_name}** from {game_name} game'
                                                    f' has been deleted from the database')
        else:
            await interaction.response.send_message(f'Map **{map_name}** from {game_name} game is not in the database,'
                                                    f' use `/add_map` to add it.')

    @nextcord.slash_command(name='get_all_maps', guild_ids=[218510314835148802])
    async def get_all_maps(self, interaction: nextcord.Interaction, game_name: str):
        """
        Command used to check player's rank and display information about it

            Args:
                interaction (nextcord.Interaction): Context of the command
                game_name (str): Name of the game that You want to get maps from

            Returns:
                None
        """
        collection = await DatabaseSettings.db_connection('Mapiez_Database', 'Maps', interaction=interaction)

        if collection is None:
            return

        if collection.count_documents({'game_name': game_name}) <= 0:
            await interaction.response.send_message(f'**{game_name}** is not in the database,'
                                                    f' or there isn\'t any map for this game', ephemeral=True)
            return

        map_list = ''
        maps = collection.find({'game_name': game_name})
        for available_map in maps:
            map_list = map_list + ':crossed_swords: ' + available_map['map_name'] + '\n'

        await interaction.response.send_message(f'**Available maps:** \n{map_list}')

    @nextcord.slash_command(name='get_all_games', guild_ids=[218510314835148802])
    async def get_all_games(self, interaction: nextcord.Interaction):
        collection = await DatabaseSettings.db_connection('Mapiez_Database', 'Maps', interaction=interaction)

        if collection is None:
            return

        games_list = ''
        games = collection.distinct('game_name')
        for game in games:
            games_list = games_list + ':crossed_swords: ' + str(game) + '\n'

        await interaction.response.send_message(f'**Available games:** \n{games_list}')

    # @nextcord.slash_command(name='update', guild_ids=[955933461959569418, 218510314835148802], force_global=True)
    # async def update(self, interaction: nextcord.Interaction):
    #     collection = await DatabaseSettings.db_connection('Mapiez_Database', 'Maps', interaction=interaction)
    #     maps = collection.find()
    #     for mapa in maps:
    #         collection.update_one({'map_name': mapa['map_name']},
    #                               {'$set':{'game_name': 'Dawn of War: Soulstorm'}})


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def channel_check(interaction: nextcord.Interaction):
        """
        Utility method that is used to check if user is sending commands in channel that allows it

            Args:
                interaction (nextcord.Interaction): ???

            Returns:
                bool: True if user can send messages in this channel, False otherwise
        """
        channel_check = False
        collection = await DatabaseSettings.db_connection('Mapiez_Database', 'Channels', interaction=interaction)
        if collection is None:
            return
        check = collection.find_one({'_id': interaction.guild_id})
        if not check:
            channel_check = True
        else:
            for bot_channel in check['bot_channels']:
                if interaction.channel_id == int(bot_channel):
                    channel_check = True

        # sends specific message if command is used in forbidden channel
        if not channel_check:
            await interaction.response.send_message(f'Please, use bot commands in bot channel to prevent spam',
                                                    ephemeral=True)
        return channel_check


def setup(client):
    client.add_cog(MapManager(client))
    client.add_cog(Utility(client))
