import asyncio
import json
import random

from redbot.core import bank, commands
from redbot.core.commands import Cog
from redbot.core.data_manager import bundled_data_path


class RecyclingPlant(Cog):
    """Apply for a job at the recycling plant!"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.junk = None

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def load_junk(self):
        junk_path = bundled_data_path(self) / "junk.json"
        with junk_path.open() as json_data:
            self.junk = json.load(json_data)

    @commands.command(aliases=["recycle"])
    async def recyclingplant(self, ctx: commands.Context):
        """Apply for a job at the recycling plant!"""
        if self.junk is None:
            self.load_junk()

        x = 0
        totalreward = 0
        timeoutcount = 0
        await ctx.send(
            "{0} has signed up for a shift at the Recycling Plant! Type `exit` to stop working.".format(
                ctx.author.display_name
            )
        )
        while x in range(0, 500):
            used = random.choice(self.junk["can"])
            if used["action"] == "trash":
                opp = "recycle"
            else:
                opp = "trash"
            await ctx.send(
                "`{}`! Will {} `trash` it or `recycle` it?".format(
                    used["object"], ctx.author.display_name
                )
            )

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                answer = await self.bot.wait_for("message", timeout=20, check=check)
            except asyncio.TimeoutError:
                answer = None

            if answer is None:
                if timeoutcount == 2:
                    await ctx.send(
                        "{} slacked off at work, so they were shot multiple times in the occipital lobe.".format(
                            ctx.author.display_name
                        )
                    )
                    break
                else:
                    await ctx.send(
                        "{} is slacking, and if they carry on not working, they'll be executed.".format(
                            ctx.author.display_name
                        )
                    )
                    timeoutcount += 1
            elif answer.content.lower().strip() == used["action"]:
                await ctx.send(
                    "Congratulations! You have the intelligence of a third grader! (**+15**)".format(
                        used["object"]
                    )
                )
                await bank.deposit_credits(ctx.author, 15)
                totalreward += 15
                x += 1
            elif answer.content.lower().strip() == opp:
                await ctx.send(
                    "no you dope"
                )
                await bank.withdraw_credits(ctx.author, 2)
                totalreward -= 2
            elif answer.content.lower().strip() == "exit":
                await ctx.send(
                    "You have been given a total of **{} {}** for your services.".format(
                        totalreward, await bank.get_currency_name(ctx.guild)
                    )
                )
                break
            else:
                await ctx.send(
                    "`{}` fell down the conveyor belt to be sorted again!".format(used["object"])
                )
        else:
            await ctx.send(
                "You have been given a total of **{} {}** for your services.".format(
                    totalreward, await bank.get_currency_name(ctx.guild)
                )
            )
