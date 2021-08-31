import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, PROB_QUESTIONS_LINES

problems = {}
for line in PROB_QUESTIONS_LINES:
    problems[line.split(' => ')[0]] = line.split(' => ')[1]

class Probability(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="probq", help="Answer a probability question")
    async def probq(self, ctx):
        random_question, random_answer = random.choice(list(problems.items()))
        try:
            preview(random_question, viewer="file", filename="generated_latex/output.png")
            await ctx.send(file=discord.File(f"./generated_latex/output.png", filename="LaTeX_output.png"))
        except:
            await ctx.send("Please slow down!")
            return

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await self.bot.wait_for("message", check=check)
        if msg.content == random_answer:
            try:
                preview("Nice job!", viewer="file", filename="generated_latex/output.png")
                await ctx.send(file=discord.File(f"./generated_latex/output.png", filename="LaTeX_output.png"))
            except:
                await ctx.send("Nice job!")
        elif msg.content in COMMAND_LIST:
            pass
        else:
            try:
                preview(f"Oof! The correct answer is {random_answer}", viewer="file", filename="generated_latex/output.png")
                await ctx.send(file=discord.File(f"./generated_latex/output.png", filename="LaTeX_output.png"))
            except:
                pass

def setup(bot):
    bot.add_cog(Probability(bot))