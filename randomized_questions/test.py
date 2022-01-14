# File for testing randomized questions

import discord
import random
from sympy import *
from discord.ext import commands
from globals import extended_format, send_and_check

random_problems = {
        'The creator of the newest protein shake fad diet claims her users have lost 10\% of their body ' +
        'weight, with a standard deviation of &(a&)\%. To see whether this diet actually works for ' +
        'everybody, you survey &(b&) dieters. The sample standard deviation is &(c&)\%. Find the ' +
        'p-value of this test.=>&(2*(1-@(chicdf((b-1)*c**2/a**2,b-1)@))&)':
        {'a': 'randuni(1,2,2)', 'b': 'randint(10,15)', 'c': 'randuni(2.2,3.2,2)'},
    }


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test", help="Testing purposes")
    async def test(self, ctx):
        random_question, variables = random.choice(list(random_problems.items()))
        formatted_question, formatted_answer = extended_format(random_question, variables)
        await send_and_check(formatted_question, formatted_answer, self.bot, ctx)

def setup(bot):
    bot.add_cog(Test(bot))