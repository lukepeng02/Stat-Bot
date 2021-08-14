import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, extended_format

random_problems = {'Let $X\sim B(&(a&),&(r&))$. Find $P[X=&(b&)]$' +
        '=>&(binomial(a, b) * (r ** b) * ((1 - r) ** (a - b))&)':
        {'a': 'randint(10,20)', 'r': 'randuni(0.2, 0.8, 2)', 'b': 'randint(2,6)'},

        'Let $X\sim B(&(a&),&(r&))$. Find the variance.=>&(a * r * (1 - r)&)':
        {'a': 'randint(10,20)', 'r': 'randuni(0.2, 0.8, 2)'},

        'I roll a fair &(c&)-sided die until I get a two &(b&) times. Find the standard deviation ' +
        'of the number of rolls.=>&(sqrt(b * (1 - (1 / c)) / ((1 / c) ** 2))&)':
        {'b': 'randint(2,6)', 'c': 'randint(6,10)'},

        'I blink according to a Poisson process with a rate of &(d&) blinks per minute. Find ' +
        'the probability I blink &(e&) times in the next &(f&) minutes.' +
        '=>&(((d * f) ** e) * exp(-1 * d * f) / factorial(e)&)':
        {'d': 'randint(16,25)', 'e': 'randint(70,130)', 'f': 'randint(4,6)'},

        'I blink according to a Poisson process with a rate of &(d&) blinks per minute. Find the ' +
        'variance in the amount of time it takes to blink &(e&) times, in minutes squared.' +
        '=>&(e * ((1 / d) ** 2)&)': {'d': 'randint(16,25)', 'e': 'randint(70,130)'},

        'Zoe receives phone calls according to a Poisson ' +
        'process with a rate of &(g&) calls per hour. Find the probability it takes more than &(h&) ' +
        'minutes for her to receive her first one.=>&(exp(-1 * g * h / 60)&)':
        {'g': 'randuni(2.0, 3.0, 1)', 'h': 'randint(20,40)'},

        'Zoe receives phone calls according to a Poisson process with a rate of &(g&) calls per ' +
        'hour. Find the probability it takes less than &(h&) minutes for her to receive her first one.' +
        '=>&(1 - exp(-1 * g * h / 60)&)':
        {'g': 'randuni(2.0, 3.0, 1)', 'h': 'randint(20,40)'},
        
        'Let $X\sim N(&(d&), &(h&))$. $P[X<&(a&)]$ is equivalent to $P[Z<a]$. Find a.' +
        '=>&((a - d) / sqrt(h)&)':
        {'d': 'randint(16,25)', 'h': 'randint(20,40)', 'a': 'randint(10,20)'},

        'Let $X\sim N(&(d&), &(h&))$ and $Y\sim N(&(a&), &(b&))$. Let $Z=&(j&)X+&(f&)Y\sim N(a,b)$. '
        'Find $ab$.=>&((j * d + f * a) * (j ** 2 * h + f ** 2 * b)&)':
        {'d': 'randint(16,25)', 'h': 'randint(20,40)', 'a': 'randint(10,20)',
        'f': 'randint(4,6)', 'b': 'randint(2,6)', 'j': 'randint(2,3)'},

        'Zoe receives phone calls according to a Poisson process with a rate of &(l&) calls per hour. ' +
        'Find the probability it takes between 1 and 2 hours for her to receive her &(a&)th one.' +
        '=>&(integrate((l ** a) / factorial(a-1) * (x ** (a - 1)) * exp(-x * l), (x, 1, 2))&)':
        {'a': 'randint(4,7)', 'l': 'randuni(3.0,4.0,1)'},
        }

class Distributions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="distq", help="Answer a distribution question")
    async def distq(self, ctx):
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
    bot.add_cog(Distributions(bot))