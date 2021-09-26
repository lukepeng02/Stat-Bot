# File for testing randomized questions

import discord
import random
from sympy import *
from discord.ext import commands
from globals import extended_format, send_and_check

random_problems = {
        'A survey of &(a&) people was conducted. The difference in the number of Kleenex used daily in ' +
        'the summer and winter was recorded for each person. The average was &(b&) Kleenex, and the ' +
        'standard deviation was &(d&). Find the lower confidence limit of a &(100-c&)$\%$ confidence ' +
        'interval for the true average difference in the number of Kleenex used daily in the summer and ' +
        'winter.=>&(b+@(tinv(c/200,a-1)@)*d/sqrt(a)&)':
        {'a': 'randint(30,40)', 'b': 'randint(-10,-5)', 'c': 'randint(2,10)', 'd': 'randint(3,5)'},
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