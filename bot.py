import random
import math
import discord
import os
from sympy import *
from discord.ext import commands

init_printing(use_latex='mathjax')

try:
    os.mkdir("generated_latex")
except FileExistsError:
    print("generated_latex directory already exists")

misc_prob_questions = open("hardcoded/misc_prob_questions.txt", 'r')
misc_prob_questions_lines = misc_prob_questions.read().splitlines()
misc_prob_questions.close()

bivar_questions = open("hardcoded/bivarq.txt", 'r')
bivar_questions_lines = bivar_questions.read().splitlines()
bivar_questions.close()

COMMAND_LIST = ['!help', '!ansformat', '!probq', '!miscprobq', '!distq', '!bivarq', '!peq']

bot = commands.Bot(command_prefix='!')

@bot.command(name="ansformat", help="Learn how to format answers")
async def ansformat(ctx):
    await ctx.send("Round numerical answers to 4 decimal places, or less if fewer are needed")
    await ctx.send("Include a zero before the decimal point if necessary")
    await ctx.send("If an answer does not have any digits but 0 when rounded to 4 places, " +
    "enter '0.0'")
    await ctx.send("Omit all 0s after the last non-zero digit, even if it is rounded")

bot.load_extension("randomized_questions.prob_questions")
bot.load_extension("randomized_questions.misc_prob_questions")
bot.load_extension("randomized_questions.dist_questions")
bot.load_extension("randomized_questions.bivar_dist_questions")
bot.load_extension("randomized_questions.point_est_questions")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)