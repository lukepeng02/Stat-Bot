import discord
import random
import math
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST

class Distributions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="distq", help="Answer a distribution question")
    async def distq(self, ctx):
        a_i = random.randint(10, 20)
        b_i = random.randint(2, 6)
        c_i = random.randint(6, 10)
        d_i = random.randint(16, 25)
        e_i = random.randint(70, 130)
        f_i = random.randint(4, 6)
        g_t = round(random.uniform(2.0, 3.0), 1)
        h_i = random.randint(20, 40)
        j_i = random.randint(2, 3)
        r_p = round(random.uniform(0.2, 0.8), 2)
        problems = {f'Let $X\sim B({a_i},{r_p})$. Find $P[X={b_i}]$':
        f'{round(math.comb(a_i, b_i) * (r_p ** b_i) * ((1 - r_p) ** (a_i - b_i)), 4)}',

        f'Let $X\simB({a_i},{r_p})$. Find the variance.': f'{round(a_i * r_p * (1 - r_p), 4)}',

        f'I roll a fair {c_i}-sided die until I get a two {b_i} times. Find the standard deviation ' +
        'of the number of rolls.': f'{round(math.sqrt(b_i * (1 - (1 / c_i)) / ((1 / c_i) ** 2)), 4)}',

        f'I blink according to a Poisson process with a rate of {d_i} blinks per minute. Find ' +
        f'the probability I blink {e_i} times in the next {f_i} minutes.':
        f'{round(((d_i * f_i) ** e_i) * math.exp(-1 * d_i * f_i) / math.factorial(e_i), 4)}',

        f'I blink according to a Poisson process with a rate of {d_i} blinks per minute. Find the ' +
        f'variance in the amount of time it takes to blink {e_i} times, in minutes squared.':
        f'{round(e_i * ((1 / d_i) ** 2), 4)}',

        'Zoe receives phone calls according to a Poisson ' +
        f'process with a rate of {g_t} calls per hour. Find the probability it takes more than {h_i} ' +
        'minutes for her to receive her first one.': f'{round(math.exp(-1 * g_t * h_i / 60), 4)}',

        f'Zoe receives phone calls according to a Poisson process with a rate of {g_t} calls per ' +
        f'hour. Find the probability it takes less than {h_i} minutes for her to receive her first one.':
        f'{round(1 - math.exp(-1 * g_t * h_i / 60), 4)}',

        'Zoe receives phone calls according to a Poisson process with a rate of 4 calls per hour. ' +
        'Find the probability it takes between 1 and 2 hours for her to receive her sixth one.':
        '0.5939', f'Let $X\sim N{d_i, h_i}$. $P[X<{a_i}]$ is equivalent to $P[Z<a]$. Find a.':
        f'{round((a_i - d_i) / math.sqrt(h_i), 4)}',

        f'Let $X\sim N{d_i, h_i}$ and $Y\sim N{a_i, b_i}$. Let $Z={j_i}X+{f_i}Y\sim N(a,b)$. Find ab.':
        f'{round((j_i * d_i + f_i * a_i) * (j_i ** 2 * h_i + f_i ** 2 * b_i), 4)}'}

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
    bot.add_cog(Distributions(bot))