# File for testing randomized questions

import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, extended_format

random_problems = {
        'Let $\sigma_X=&(a&), \sigma_Y=&(b&)$, and $\\rho_{XY}=&(e&)$. Find $Var[&(c&)X-&(d&)Y]$.' +
        '=>&((a**2*c**2+b**2*d**2-2*a*b*c*d*e)&)':
        {'a': 'randint(3,7)', 'b': 'randint(3,7)', 'c': 'randint(2,5)', 'd': 'randint(2,5)',
        'e': 'randuni(0.01,0.99,2)'},
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