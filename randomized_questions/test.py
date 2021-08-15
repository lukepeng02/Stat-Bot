# File for testing randomized questions

import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, extended_format

random_problems = {
        'Tom the Turkey lives in a coop with &(c&) other turkeys. This Thanksgiving season, &(b&) turkeys ' +
        'are randomly ``selected" every day and replaced with other turkeys. What is the probability ' +
        'Tom is ``selected" on day &(a&)?=>&((1 - b / (c + 1)) ** (a - 1) * (b / (c + 1))&)':
        {'a': 'randint(2,10)', 'b': 'randint(20,80)' ,'c': 'randint(249, 349)'},
        }


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test", help="Testing purposes")
    async def test(self, ctx):
        random_question, variables = random.choice(list(random_problems.items()))
        formatted_question, formatted_answer = extended_format(random_question, variables)

        try:
            preview(formatted_question, viewer="file", filename="generated_latex/output.png")
            await ctx.send(file=discord.File(f"./generated_latex/output.png", filename="LaTeX_output.png"))
        except:
            await ctx.send("Please slow down!")
            return

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