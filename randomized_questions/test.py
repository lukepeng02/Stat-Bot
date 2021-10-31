# File for testing randomized questions

import discord
import random
from sympy import *
from discord.ext import commands
from globals import extended_format, send_and_check

random_problems = {
'A survey of &(a&) fans of Enlightenment (a famous grunge band) was conducted. ' +
        'Of these, &(d&) believed the band made better music than Pistols and Poppies, a ' +
        'hard rock band, but had never even listened to a single Pistols and Poppies song. ' +
        'Find the upper limit of a &(100-c&)$\%$ confidence interval for the proportion of all ' +
        'Enlightenment fans who believed the band made better music than Pistols and Poppies, but ' +
        'had never even listened to any of their songs.' +
        '=>&(d/a-(@(norminv(c/200,0,1)@)*sqrt((d/a*(1-d/a)/a)))&)':
        {'a': 'randint(150,200)', 'c': 'randint(2,10)', 'd': 'randint(60,75)'},
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