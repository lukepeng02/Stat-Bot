import discord
import random
import math
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, MISC_PROB_QUESTIONS_LINES

class Misc_Probability(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="miscprobq", help="Answer a miscellaneous probability question")
    async def miscprobq(self, ctx):
        f_i = random.randint(2, 6)
        s_i = random.randint(2, 6)
        t_i = random.randint(2, 6)
        d_i = random.randint(10, 20)
        e_i = random.randint(6, 10)

        f_f = round(random.uniform(0.5, 0.7), 2)
        s_f = round(random.uniform(0.5, 0.7), 2)
        t_f = round(random.uniform(0.4, min(f_f, s_f)), 2)

        problems = {f'I have {f_i + s_i + t_i} cards: {f_i} are red ' +
            f'on both sides, {s_i} are blue on both sides, and {t_i} are blue on one ' +
            'side and red on the other. I choose a random card and see it is red on this side. ' +
            'What is the probability the other side is blue?': f'{round(t_i / (2 * f_i + t_i), 4)}',

            f'The probability David takes the bus on any day is {f_f}, and the probability it ' +
            f'rains on any day is {s_f}. If the probability that it is not raining and David is ' +
            f'not taking the bus is {round(1 - f_f - s_f + t_f, 2)}, find the probability it ' +
            'is raining, given David is not taking the bus.': f'{round((s_f - t_f) / (1 - f_f), 4)}',

            f'Let the pmf of $f(x)=c\cdot\\frac{{{f_i}^x}}{{x!}}, x = 3,4,5,...$ What is $c$?':
            f'{round(2 / (2 * math.exp(f_i) - f_i ** 2 - 2 * f_i - 2), 4)}',

            f'I roll a fair six-sided die {d_i} times. What is $P$[exactly {f_i} perfect squares]?':
            f'{round(math.comb(d_i, f_i) * ((1 / 3) ** f_i) * ((2 / 3) ** (d_i - f_i)), 4)}',

            f'I roll a fair {e_i}-sided die {f_i} times. What is the expected value for the product?':
            f'{round(((e_i + 1) / 2) ** f_i, 4)}'}
        
        for line in MISC_PROB_QUESTIONS_LINES:
            problems[line.split(' => ')[0]] = line.split(' => ')[1]

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
    bot.add_cog(Misc_Probability(bot))