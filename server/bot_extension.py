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
    async def icons(self, interaction: discord.Interaction):
        '''
        Shows the current Nintendo Switch Online icons!
        '''
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
        for icon in self.icons[:24]:
            embed.add_field(
                name = '%s' % icon[1],
                value = '[%s Icon](%s%s)' % (icon[0], self.url, icon[2]),
                inline = True,
            )
        if len(self.icons) >= 25:
            embed.add_field(
                name = 'And more!',
                value = '[See more here](%s)' % self.url,
                inline = True,
            )
        embed.set_footer(
            text = 'Provided by nso-applet-api',
        )
        await interaction.response.send_message(embed = embed)

async def setup(bot):
    await bot.add_cog(NSO_IconDB(bot))
