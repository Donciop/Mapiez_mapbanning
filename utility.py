import nextcord
from nextcord.ext import commands
import pymongo
import os


class Utility(commands.Cog):
    @staticmethod
    async def db_connection(db: str, collection: str, *, interaction: nextcord.Interaction = None):
        """
        Utility method that is used to connect to the MongoDB Database

            Args:
                db (str): Name of the Database
                collection (str): Name of the Collection in Database
                interaction (:obj:nextcord.Interaction, optional): Context of the command

            Returns:
                collection: Collection from the Database
        """
        mongo_client = pymongo.MongoClient(os.getenv('MONGOURL'))
        db = mongo_client[db]
        collection = db[collection]
        if collection is None:
            if interaction:
                await interaction.response.send_message('Cannot connect to the database', ephemeral=True)
                return
        return collection
