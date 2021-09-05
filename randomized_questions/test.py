# File for testing randomized questions

import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, extended_format

random_problems = {
        '&(a&) males (pop.1) and &(b&) females (pop.2) were asked whether they liked black licorice. &(d&) ' +
        'males and &(e&) females responded ``yes". Find the lower confidence limit of a &(100-c&)$\%$ ' +
        'confidence interval for the true difference in proportions, of people who enjoy black licorice, ' +
        'between the two groups.=>&((d/a-e/b)+@(norminv(c/200,0,1)@)* sqrt((a-d)*d/a**3+(b-e)*e/b**3)&)':
        {'a': 'randint(40,60)', 'b': 'randint(30,50)', 'c': 'randint(2,10)', 'd': 'randint(5,15)',
        'e': 'randint(0,10)'},
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