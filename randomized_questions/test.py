# File for testing randomized questions

import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, extended_format

random_problems = {
        'Ash wants to form a &(100-c&)$\%$ confidence interval with width &(a&) pound(s) for the ' +
        'average weight of a Snorlax. If the Pokédex claims the population standard deviation ' +
        'is &(b&) pounds, find the appropriate sample size of this study.' +
        '=>&(ceiling((b*@(norminv(1-c/200,0,1)@)/a)**2)&)':
        {'a': 'randuni(0.5,1,1)', 'b': 'randint(10,20)', 'c': 'randint(2,10)'},
        }


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test", help="Testing purposes")
    async def test(self, ctx):
        random_question, variables = random.choice(list(random_problems.items()))
        formatted_question, formatted_answer = extended_format(random_question, variables)

        preview(formatted_question, viewer="file", filename="generated_latex/output.png")
        await ctx.send(file=discord.File(f"./generated_latex/output.png", filename="LaTeX_output.png"))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await self.bot.wait_for("message", check=check)
        if msg.content == formatted_answer:
            try:
                preview("Nice job!", viewer="file", filename="generated_latex/output.png")
                await ctx.send(file=discord.File(f"./generated_latex/output.png", filename="LaTeX_output.png"))
            except:
                await ctx.send("Nice job!")
        elif msg.content in COMMAND_LIST:
            pass
        else:
            try:
                preview(f"Oof! The correct answer is {formatted_answer}", viewer="file", filename="generated_latex/output.png")
                await ctx.send(file=discord.File(f"./generated_latex/output.png", filename="LaTeX_output.png"))
            except:
                pass

def setup(bot):
    bot.add_cog(Test(bot))