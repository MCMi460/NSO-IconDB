# Made by Deltaion Lee (MCMi460) on Github
# This script is an extension for Discord bots written in discord.py
import discord, sys, os
from discord.ext import commands, tasks
sys.path.append('./NSO-IconDB/server')
from backend import main, getCurrentIcons

class NSO_IconDB(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.icons = []
        self.url = 'https://icondb.nsorpc.com'

    def embed_constructor(self, n = 0):
        embed = discord.Embed(
            title = 'Nintendo Switch Online Icons Database',
            url = 'https://icondb.nsorpc.com/',
            description = 'Current Icons on the NSO Applet',
            color = 0xe60012,
        )
        embed.set_author(
            name = 'MCMi460',
            url = 'https://github.com/MCMi460',
            icon_url = 'https://avatars.githubusercontent.com/u/32529306',
        )
        for icon in self.icons[n * 25:(n + 1) * 25]:
            embed.add_field(
                name = '%s' % icon[1],
                value = '[%s Icon](%s%s)' % (icon[0], self.url, icon[2]),
                inline = True,
            )
        embed.set_footer(
            text = 'Provided by nso-applet-api',
        )
        return embed

    class Buttons(discord.ui.View):
        def __init__(self, *,
            timeout = 180,
            icons = [],
            index = 0,
            embed_constructor = None,
        ):
            super().__init__(timeout = timeout)
            self.icons = icons
            self.index = index
            self.embed_constructor = embed_constructor

            self.check(0)

        def check(self, n):
            if self.icons > (n + 1) * 25:
                self.children[1].disabled = False
                self.children[1].style = discord.ButtonStyle.blurple
            else:
                self.children[1].disabled = True
                self.children[1].style = discord.ButtonStyle.red

            if n > 0:
                self.children[0].disabled = False
                self.children[0].style = discord.ButtonStyle.blurple
            else:
                self.children[0].disabled = True
                self.children[0].style = discord.ButtonStyle.red

        @discord.ui.button(
            label = '⬅️',
            style = discord.ButtonStyle.red,
            disabled = True,
        )
        async def left_button(self, interaction:discord.Interaction, button:discord.ui.Button):
            self.index -= 1
            embed = self.embed_constructor(self.index)
            self.check(self.index)
            await interaction.response.edit_message(
                embed = embed,
                view = self,
            )

        @discord.ui.button(
            label = '➡️',
            style = discord.ButtonStyle.red,
            disabled = True,
        )
        async def right_button(self, interaction:discord.Interaction, button:discord.ui.Button):
            self.index += 1
            embed = self.embed_constructor(self.index)
            self.check(self.index)
            await interaction.response.edit_message(
                embed = embed,
                view = self,
            )

    @commands.Cog.listener()
    async def on_ready(self):
        print('[NSO-IconDB ready]')
        self.backend.start()

    @tasks.loop(seconds = 3600)
    async def backend(self):
        os.chdir('./NSO-IconDB/server')
        try:
            main()
        except Exception as e:
            print(e)
        self.icons = getCurrentIcons()
        os.chdir('../../')

    @discord.app_commands.command()
    @discord.app_commands.checks.cooldown(1, 10) # Try to prevent spamming of this command
    async def icons(self, interaction: discord.Interaction, hidden:bool = False):
        '''
        Shows the current Nintendo Switch Online icons!
        '''
        embed = self.embed_constructor(0)
        await interaction.response.send_message(
            embed = embed,
            view = self.Buttons(
                icons = len(self.icons),
                embed_constructor = self.embed_constructor,
            ),
            ephemeral = hidden,
        )

    @icons.error
    async def icons_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral = True)

async def setup(bot):
    await bot.add_cog(NSO_IconDB(bot))
