import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, extended_format

random_problems = {
        'Consider $X_1,...,X_5$ with $f(x;p)=pe^{-px^2}, x>0, p>0$. Find the MLE ' +
        'estimator of $p$ when $x_1 = &(a&), x_2 = &(b&), x_3 = &(c&), x_4 = &(d&), x_5 = &(e&)$' +
        '=>&(5 / (a ** 2 + b ** 2 + c ** 2 + d ** 2 + e ** 2)&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)',
        'e': 'randint(3,6)'},

        'Consider $X_1,...,X_4$ with $f(x;t)=2t^2\cdot x e^{x^2/t}\cdot3^x, x>0, t>0$. Find the MLE ' +
        'estimator of $t$ when $x_1 = &(a&), x_2 = &(b&), x_3 = &(c&), x_4 = &(d&)$' +
        '=>&((a ** 2 + b ** 2 + c ** 2 + d ** 2) / 8&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)'},

        'Consider $X_1,...,X_4$ with $f(x)=\\frac{2p-x}{2p^2}, 0<x<2p, p>0$. Find the MOM ' +
        'estimator of $p$ when $x_1 = &(a&), x_2 = &(b&), x_3 = &(c&), x_4 = &(d&)$' +
        '=>&(3 * (a + b + c + d) / 8&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)'},

        'Consider $X_1,...,X_5$ with $f(x)=8\cdot\\frac{3t-4x}{9t^2}, 0<x<\\frac{3t}{4}, t>0$. Find the MOM ' +
        'estimator of $t$ when $x_1 = &(a&), x_2 = &(b&), x_3 = &(c&), x_4 = &(d&), x_5 = &(e&)$' +
        '=>&(4 * (a + b + c + d + e) / 5&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)',
        'e': 'randint(3,6)'},
        }


class Point_Estimation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="peq", help="Answer a point estimation question")
    async def peq(self, ctx):
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
    bot.add_cog(Point_Estimation(bot))