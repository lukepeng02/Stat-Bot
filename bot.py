import random
import math
import discord
from sympy import *
from discord.ext import commands

init_printing(use_latex='mathjax')

prob_questions = open("prob_questions.txt", 'r')
prob_questions_lines = prob_questions.read().splitlines()
prob_questions.close()

misc_prob_questions = open("misc_prob_questions.txt", 'r')
misc_prob_questions_lines = misc_prob_questions.read().splitlines()
misc_prob_questions.close()

bivar_questions = open("bivarq.txt", 'r')
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

@bot.command(name="probq", help="Answer a random probability question")
async def probq(ctx):
    problems = {}
    for line in prob_questions_lines:
        problems[line.split(' => ')[0]] = line.split(' => ')[1]

    random_question, random_answer = random.choice(list(problems.items()))
    preview(random_question, viewer="file", filename="output.png")
    await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content == random_answer:
        try:
            preview("Nice job!", viewer="file", filename="output.png")
            await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))
        except:
            await ctx.send("Nice job!")
    elif msg.content in COMMAND_LIST:
        pass
    else:
        try:
            preview(f"Oof! The correct answer is {random_answer}", viewer="file", filename="output.png")
            await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))
        except:
            pass

@bot.command(name="miscprobq", help="Answer a miscellaneous probability question")
async def miscprobq(ctx):
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
    
    for line in misc_prob_questions_lines:
        problems[line.split(' => ')[0]] = line.split(' => ')[1]

    random_question, random_answer = random.choice(list(problems.items()))
    preview(random_question, viewer="file", filename="output.png")
    await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content == random_answer:
        try:
            preview("Nice job!", viewer="file", filename="output.png")
            await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))
        except:
            await ctx.send("Nice job!")
    elif msg.content in COMMAND_LIST:
        pass
    else:
        try:
            preview(f"Oof! The correct answer is {random_answer}", viewer="file", filename="output.png")
            await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))
        except:
            pass

@bot.command(name="distq", help="Answer a distribution question")
async def distq(ctx):
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
    preview(random_question, viewer="file", filename="output.png")
    await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content == random_answer:
        try:
            preview("Nice job!", viewer="file", filename="output.png")
            await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))
        except:
            await ctx.send("Nice job!")
    elif msg.content in COMMAND_LIST:
        pass
    else:
        try:
            preview(f"Oof! The correct answer is {random_answer}", viewer="file", filename="output.png")
            await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))
        except:
            pass

@bot.command(name="bivarq", help="Answer a bivariate distribution question")
async def bivarq(ctx):
    problems = {}
    for line in bivar_questions_lines:
        problems[line.split(' => ')[0]] = line.split(' => ')[1]

    random_question, random_answer = random.choice(list(problems.items()))
    preview(random_question, viewer="file", filename="output.png")
    await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content == random_answer:
        try:
            preview("Nice job!", viewer="file", filename="output.png")
            await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))
        except:
            await ctx.send("Nice job!")
    elif msg.content in COMMAND_LIST:
        pass
    else:
        try:
            preview(f"Oof! The correct answer is {random_answer}", viewer="file", filename="output.png")
            await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))
        except:
            pass

@bot.command(name="peq", help="Answer a point estimation question")
async def peq(ctx):
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
    preview(random_question, viewer="file", filename="output.png")
    await ctx.send(file=discord.File("./output.png", filename="LaTeX_output.png"))

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content == random_answer:
        try:
            preview("Nice job!", viewer="file", filename="output.png")
            await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))
        except:
            await ctx.send("Nice job!")
    elif msg.content in COMMAND_LIST:
        pass
    else:
        try:
            preview(f"Oof! The correct answer is {random_answer}", viewer="file", filename="output.png")
            await ctx.send(file=discord.File(f"./output.png", filename="LaTeX_output.png"))
        except:
            pass

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)