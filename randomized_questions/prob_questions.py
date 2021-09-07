import discord
import random
from sympy import *
from discord.ext import commands
from globals import PROB_QUESTIONS_LINES, send_and_check

problems = {}
for line in PROB_QUESTIONS_LINES:
    problems[line.split(' => ')[0]] = line.split(' => ')[1]

class Probability(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="probq", help="Answer a probability question")
    async def probq(self, ctx):
        formatted_question, formatted_answer = random.choice(list(problems.items()))

        await send_and_check(formatted_question, formatted_answer, self.bot, ctx)

def setup(bot):
    bot.add_cog(Probability(bot))