import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST

class Point_Estimation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="peq", help="Answer a point estimation question")
    async def peq(self, ctx):
        a_i = random.randint(3, 6)
        b_i = random.randint(3, 6)
        c_i = random.randint(3, 6)
        d_i = random.randint(3, 6)
        e_i = random.randint(3, 6)
        problems = {'Consider $X_1,...,X_5$ with $f(x;p)=pe^{-px^2}, x>0, p>0$. Find the MLE ' +
        f'estimator of $p$ when $x_1 = {a_i}, x_2 = {b_i}, x_3 = {c_i}, x_4 = {d_i}, x_5 = {e_i}$':
        f'{round(5 / (a_i ** 2 + b_i ** 2 + c_i ** 2 + d_i ** 2 + e_i ** 2), 4)}',

        'Consider $X_1,...,X_4$ with $f(x;t)=2t^2\cdot x e^{x^2/t}\cdot3^x, x>0, t>0$. Find the MLE ' +
        f'estimator of $t$ when $x_1 = {a_i}, x_2 = {b_i}, x_3 = {c_i}, x_4 = {d_i}$':
        f'{round((a_i ** 2 + b_i ** 2 + c_i ** 2 + d_i ** 2) / 8, 4)}',

        'Consider $X_1,...,X_4$ with $f(x)=\\frac{2p-x}{2p^2}, 0<x<2p, p>0$. Find the MOM ' +
        f'estimator of $p$ when $x_1 = {a_i}, x_2 = {b_i}, x_3 = {c_i}, x_4 = {d_i}$':
        f'{3 * (a_i + b_i + c_i + d_i) / 8}',

        'Consider $X_1,...,X_5$ with $f(x)=8\cdot\\frac{3t-4x}{9t^2}, 0<x<\\frac{3t}{4}, t>0$. Find the MOM ' +
        f'estimator of $t$ when $x_1 = {a_i}, x_2 = {b_i}, x_3 = {c_i}, x_4 = {d_i}, x_5 = {e_i}$':
        f'{4 * (a_i + b_i + c_i + d_i + e_i) / 5}'}

        random_question, random_answer = random.choice(list(problems.items()))
        preview(random_question, viewer="file", filename="generated_latex/output.png")
        await ctx.send(file=discord.File(f"./generated_latex/output.png", filename="LaTeX_output.png"))

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
    bot.add_cog(Point_Estimation(bot))