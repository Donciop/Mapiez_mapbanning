import nextcord
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
from db_operations import Utility
import random

VIEW_NAME = "RoleView"


def custom_id(view: str, id: int):
    return f"{view}:{id}"


class BanView(nextcord.ui.View):
    def __init__(self, first_player, second_player, best_of):
        super().__init__(timeout=None)
        self.first_player = first_player
        self.second_player = second_player
        self.best_of = best_of
        self.maps_left = 11
        self.first_player_bool = True
        self.second_player_bool = False

    async def button_callback(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if self.maps_left <= self.best_of:
            self.first_player_bool = False
            self.second_player_bool = False
            embed = nextcord.Embed(title=':crossed_swords: Mapy zostały wybrane')
            await interaction.response.edit_message(embed=embed, view=self)
            return
        if interaction.user == self.first_player and self.first_player_bool:
            button.disabled = True
            button.style = nextcord.ButtonStyle.danger
            self.first_player_bool = False
            self.second_player_bool = True
            self.maps_left -= 1
            embed = nextcord.Embed(
                title=f'Mapa **{button.label}** została zbanowana przez **{interaction.user.display_name}**!',
                description=f'Kolejny banuje **{self.second_player.display_name}**')
            await interaction.response.edit_message(embed=embed, view=self)
        elif interaction.user == self.second_player and self.second_player_bool:
            button.disabled = True
            button.style = nextcord.ButtonStyle.danger
            self.first_player_bool = True
            self.second_player_bool = False
            self.maps_left -= 1
            embed = nextcord.Embed(
                title=f'Mapa **{button.label}** została zbanowana przez **{interaction.user.display_name}**!',
                description=f'Kolejny banuje **{self.first_player.display_name}**'
            )
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await interaction.response.send_message('Poczekaj na swoją kolej banowania', ephemeral=True)

    @nextcord.ui.button(label='Battle Marshes (BM)', emoji='<:BM:980399980382679060>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 1))
    async def first_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Fallen City Remastered (FC)', emoji='<:FC:980399980768534588>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 2))
    async def second_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Fata Morga Remastered (FM)', emoji='<:FM:980399980802105344>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 3))
    async def third_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Quest’s Triumph (QT)', emoji='<:QT:980399980588199986>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 4))
    async def fourth_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Shrine of Excellion Remastered (SoE)', emoji='<:SoE:980399980852437033>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 5))
    async def fifth_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Titan’s Fall Remastered (TF)', emoji='<:TiF:980399980978245632>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 6))
    async def sixth_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Tranqulity’s End Remastered (TE)', emoji='<:TE:980399980739198997>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 7))
    async def seventh_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Frazier\'s Demise (FD)', emoji='<:FD:980399980672090132>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 8))
    async def eight_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Bloody Hell [Ed]', emoji='<:BH:980399979954864179>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 9))
    async def nine_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Blood River Remastered (BR)', emoji='<:BR:980399981410254868>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 10))
    async def ten_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Deadly Fun Archeology (DFA)', emoji='<:DFA:980399981338984468>',
                        style=nextcord.ButtonStyle.green,
                        custom_id=custom_id(VIEW_NAME, 11))
    async def eleven_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)


class FractionView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    async def button_callback(button: nextcord.Button, interaction: nextcord.Interaction):
        role_id = int(button.custom_id)
        role = interaction.guild.get_role(role_id)

        assert isinstance(role, nextcord.Role)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f'Your {role.name} role has been removed', ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f'Role {role.name} has been added', ephemeral=True)

    @nextcord.ui.button(label='Necrons', emoji='<:Necron:984435126752653373>', style=nextcord.ButtonStyle.primary,
                        custom_id=str(957267559533658132))
    async def first_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Imperial Guard', emoji='<:IG:984435125720842330>', style=nextcord.ButtonStyle.primary,
                        custom_id=str(957268227690496100))
    async def second_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Chaos', emoji='<:CSM:984435121077768223>', style=nextcord.ButtonStyle.primary,
                        custom_id=str(957268352911437846))
    async def third_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Space Marines', emoji='<:SM:984435130091311154>', style=nextcord.ButtonStyle.primary,
                        custom_id=str(957267552386572318))
    async def fourth_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Tau', emoji='<:Tau:984435133044113478>', style=nextcord.ButtonStyle.primary,
                        custom_id=str(957267555217727539))
    async def fifth_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Sisters of Battle', emoji='<:SoB:984435131358011452>', style=nextcord.ButtonStyle.primary,
                        custom_id=str(957267557407146005))
    async def sixth_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Orcs', emoji='<:Ork:984435128682029066>', style=nextcord.ButtonStyle.primary,
                        custom_id=str(957267546040574002))
    async def seventh_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Eldar', emoji='<:Eldar:984435124206719026>', style=nextcord.ButtonStyle.primary,
                        custom_id=str(957267529439518760))
    async def eight_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)

    @nextcord.ui.button(label='Dark Eldar', emoji='<:DE:984435122751275028>', style=nextcord.ButtonStyle.primary,
                        custom_id=str(957267549735764058))
    async def nineth_button(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await self.button_callback(button, interaction)


class ReactionCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name='bans', guild_ids=[955933461959569418, 218510314835148802], force_global=True)
    async def bans(self, interaction: nextcord.Interaction,
                   first_player: nextcord.Member,
                   second_player: nextcord.Member,
                   random_first: int = SlashOption(name="random",
                                                   description='Roll who will be banning first',
                                                   choices={'yes': 1, 'no': 0}),
                   best_of: int = SlashOption(name="best_of",
                                              description="Select option",
                                              choices={"bo1": 1, "bo3": 3, "bo5": 5, "bo7": 7})):
        """
        Utility config method for #role channel. Needs OWNER permissions.

            Args:
                interaction (nextcord.Interaction): Context of the command
                first_player (nextcord.Member): First player
                second_player (nextcord.Member): Second player
                random_first (int): True if You want to randomize who's banning first
                best_of (int): amount of maps left after voting

            Returns:
                None
        """
        channel_check = await Utility.channel_check(interaction)
        if not channel_check:
            return

        if random_first == 1:
            players = [first_player, second_player]
            first_player = random.choice(players)
            second_player = players[0]
        embed = nextcord.Embed(title='❌ Wybierz mapę do zbanowania',
                               description=f'Pierwszy banuje **{first_player.display_name}**')
        self.client.add_view(BanView(first_player, second_player, best_of))
        await interaction.response.send_message(embed=embed, view=BanView(first_player, second_player, best_of))

    @nextcord.slash_command(name='who_first', guild_ids=[955933461959569418, 218510314835148802], force_global=True)
    async def who_first(self,
                        interaction: nextcord.Interaction,
                        first_player: nextcord.Member,
                        second_player: nextcord.Member):
        """
        Command used to determine who's banning first between 2 players

            Args:
                interaction (nextcord.Interaction): Context of the command
                first_player (nextcord.Member): First player
                second_player (nextcord.Member): Second player

            Returns:
                None
        """
        channel_check = await Utility.channel_check(interaction)
        if not channel_check:
            return

        number = random.randint(0, 2138)
        if number > 1068:
            first_banning = second_player
        else:
            first_banning = first_player
        await interaction.response.send_message(
            f'Rzut kostką **D2137** aby sprawdzić kto pierwszy banuje.\n'
            f'Numery od `0` do `1067`, banuje **{first_player.display_name}**,'
            f' a numery od `1068` do `2137`, **{second_player.display_name}**.\n\n'
            f'Wylosowany numer to: **{number}**! Pierwszy banuje **{first_banning.display_name}**!')

    @nextcord.slash_command(name='roles', guild_ids=[955933461959569418, 926435401483309066])
    @application_checks.has_permissions(administrator=True)
    async def fractions(self, interaction: nextcord.Interaction):
        """
        Utility config method for #role channel. Needs OWNER permissions.

            Args:
               interaction (nextcord.Interaction): Context of the command

            Returns:
                None
        """
        embed = nextcord.Embed(title='Mapież Reaction Roles',
                               description='React to add or remove any role You want')
        await interaction.response.send_message(embed=embed, view=FractionView())


def setup(client):
    client.add_cog(ReactionCommands(client))
