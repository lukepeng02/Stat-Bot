import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, extended_format

random_problems = {
        'Consider $X_1,...,X_5$ with pdf $f(x;\\theta)=\\frac{{1}}{{\\theta}}e^{{-\\frac{{x}}{{\\theta}}}}, ' +
        'x\geq0, \\theta>0$. Find the MLE estimator of $\\theta$ when $x_1 = &(a&), x_2 = &(b&), ' +
        'x_3 = &(c&), x_4 = &(d&), x_5 = &(e&)$=>&((a+b+c+d+e)/5&)':
        {'a': 'randuni(-1,1,2)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)',
        'e': 'randint(3,6)'},

        }

class Confidence_Intervals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ciq", help="Answer a confidence interval question")
    async def ciq(self, ctx):
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
    bot.add_cog(Confidence_Intervals(bot))