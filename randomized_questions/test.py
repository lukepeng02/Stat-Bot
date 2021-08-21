# File for testing randomized questions

import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, extended_format

random_problems = {
        'Consider $X$ whose pmf is listed as the following ordered pairs in the format $(x,f(x))$: ' +
        '$(0,3\\theta/5), (1,2\\theta/5), (2,3(1-\\theta)/5), (3,2(1-\\theta)/5)$, where ' +
        '$\\theta\in[0,1]$. Find the MLE estimator of $\\theta$ when a sample of size 10 has the ' +
        'following observed values: &(a&) 0(s), &(b&) 1(s), &(c&) 2(s), and &(10-a-b-c&) 3(s).' +
        '=>&((12-5*(b+2*c+3*(10-a-b-c))/10)/10&)'
        : {'a': 'randint(1,4)', 'b': 'randint(0,3)', 'c': 'randint(0,3)'},
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