import discord
import random
from sympy import *
from discord.ext import commands
from globals import DELETE_EMOJI, extended_format, send_and_check

random_problems = {
            "Placeholder question: is Albert the best Stat 400 professor ever?=>yes" : {}
        }

class Hypothesis_Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not user.bot and reaction.emoji == DELETE_EMOJI:
            if reaction.message.author.id == user.id or user.mentioned_in(reaction.message):
                await reaction.message.delete()

    @commands.command(name="htq", help="Answer a hypothesis testing question")
    async def htq(self, ctx):
        random_question, variables = random.choice(list(random_problems.items()))
        formatted_question, formatted_answer = extended_format(random_question, variables)

        await send_and_check(formatted_question, formatted_answer, self.bot, ctx)

def setup(bot):
    bot.add_cog(Hypothesis_Testing(bot))