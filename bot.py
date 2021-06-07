import random
import math
from discord.ext import commands


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
    die_prefix = "A fair six-sided die is rolled. What is the probability that the outcome..."
    die_problems = {'is odd?': '0.5', 'is either even or prime?': '0.8333',
        'is a perfect square?': '0.3333'}

    dice_prefix = "Two fair six-sided dice are rolled. What is the probability that..."
    dice_problems = {'the number on one die is bigger than that on the other?': '0.8333',
        'the sum of the two dice is 7?': '0.1667',
        'the product of the two dice is at least 20?': '0.2222',
        'at least one 6 was rolled, given the product is at least 15?': '0.5385',
        'a number I choose between 2 and 12 (with equal weight) is at least the sum of the ' +
        'two dice?':
        '0.5455', 'each die has a Fibonacci number, given the sum is a Fibonacci number?':
        '0.5833'}

    card_prefix = "From a standard deck of 52 cards..."
    card_problems = {'a card is drawn. What is the probability it is the Ace of Spades?': '0.0192',
        '3 cards are drawn without replacement. What is the probability they are all spades?':
        '0.0129',
        '3 cards are drawn without replacement. What is the probability exactly 2 are of the ' +
        'same suit?':
        '0.5506', '5 cards are drawn without replacement. What is the probability 4 have ' +
        'the same number, given at least 3 have the same number?': '0.0105'}

    problems = {die_prefix: die_problems, dice_prefix: dice_problems, card_prefix: card_problems}
    random_prefix, random_questions = random.choice(list(problems.items()))
    random_question, random_answer = random.choice(list(random_questions.items()))
    await ctx.send(random_prefix + random_question)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content == random_answer:
        await ctx.send("Nice job!")
    else:
        await ctx.send("Oof! The correct answer is " + random_answer)

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
        'side and red on the other. I choose a random card and see it is red on this side. '
        'What is the probability the other side is blue?': f'{round(t_i / (2 * f_i + t_i), 4)}',
        f'The probability David takes the bus on any day is {f_f}, and the probability it ' +
        f'rains on any day is {s_f}. If the probability that it is not raining and David is ' +
        f'not taking the bus is {round(1 - f_f - s_f + t_f, 2)}, find the probability it ' +
        'is raining, given David is not taking the bus.': f'{round((s_f - t_f) / (1 - f_f), 4)}',
        f'Let the pmf of f(x)=c*({f_i}^x)/x!, x = 3,4,5,... What is c?':
        f'{round(2 / (2 * math.exp(f_i) - f_i ** 2 - 2 * f_i - 2), 4)}',
        f'I roll a fair six-sided die {d_i} times. What is P[exactly {f_i} perfect squares]?':
        f'{round(math.comb(d_i, f_i) * ((1 / 3) ** f_i) * ((2 / 3) ** (d_i - f_i)), 4)}',
        f'I roll a fair {e_i}-sided die {f_i} times. What is the expected value for the product?':
        f'{round(((e_i + 1) / 2) ** f_i, 4)}'}

    random_question, random_answer = random.choice(list(problems.items()))
    await ctx.send(random_question)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content == random_answer:
        await ctx.send("Nice job!")
    else:
        await ctx.send("Oof! The correct answer is " + random_answer)

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
    problems = {f'Let X~B({a_i},{r_p}). Find P[X={b_i}]':
    f'{round(math.comb(a_i, b_i) * (r_p ** b_i) * ((1 - r_p) ** (a_i - b_i)), 4)}',
    f'Let X~B({a_i},{r_p}). Find the variance.': f'{round(a_i * r_p * (1 - r_p), 4)}',
    f'I roll a fair {c_i}-sided die until I get a two {b_i} times. Find the standard deviation ' +
    'of the number of rolls.': f'{round(math.sqrt(b_i * (1 - (1 / c_i)) / ((1 / c_i) ** 2)), 4)}',
    f'I blink according to a Poisson process with a rate of {d_i} blinks per minute. Find ' +
    f'the probability I blink {e_i} times in the next {f_i} minutes.':
    f'{round(((d_i * f_i) ** e_i) * math.exp(-1 * d_i * f_i) / math.factorial(e_i), 4)}',
    f'I blink according to a Poisson process with a rate of {d_i} blinks per minute. Find the ' +
    f'variance in the amount of time it takes to blink {e_i} times, in minutes squared.':
    f'{round(e_i * ((1 / d_i) ** 2), 4)}', 'Zoe receives phone calls according to a Poisson ' +
    f'process with a rate of {g_t} calls per hour. Find the probability it takes more than {h_i} ' +
    'minutes for her to receive her first one.': f'{round(math.exp(-1 * g_t * h_i / 60), 4)}',
    f'Zoe receives phone calls according to a Poisson process with a rate of {g_t} calls per ' +
    'hour. Find the probability it takes less than {h_i} minutes for her to receive her first one.':
    f'{round(1 - math.exp(-1 * g_t * h_i / 60), 4)}',
    'Zoe receives phone calls according to a Poisson process with a rate of 4 calls per hour. ' +
    'Find the probability it takes between 1 and 2 hours for her to receive her sixth one.':
    '0.5939', f'Let X~N{d_i, h_i}. P[X<{a_i}] is equivalent to P[Z<a]. Find a.':
    f'{round((a_i - d_i) / math.sqrt(h_i), 4)}',
    f'Let X~N{d_i, h_i} and Y~N{a_i, b_i}. Let Z={j_i}X+{f_i}Y~N(a,b). Find ab.':
    f'{round((j_i * d_i + f_i * a_i) * (j_i ** 2 * h_i + f_i ** 2 * b_i), 4)}'}

    random_question, random_answer = random.choice(list(problems.items()))
    await ctx.send(random_question)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content == random_answer:
        await ctx.send("Nice job!")
    else:
        await ctx.send("Oof! The correct answer is " + random_answer)

@bot.command(name="bivarq", help="Answer a bivariate distribution question")
async def bivarq(ctx):
    first_prefix = "Consider f(x,y)=(x+y)/8, defined in the region x>0, y>0, y<4-2x. "
    first_problems = {'Compute E[X]': '0.6667', 'Compute E[Y]': '1.6667',
    'Compute Var[X]': '0.2222', 'Compute Var[Y]': '0.9556', 'Compute Cov[X,Y]': '-0.3111',
    'Compute E[XY]': '0.8', 'Compute P[X>1]': '0.25'}

    second_prefix = "Consider f(x,y)=(1/3)(2/3)^x(1/2)^y, defined in x=0,1,2,... and y=1,2,..."
    second_problems = {'Compute E[X]': '2', 'Compute E[Y]': '2',
    'Compute Var[X]': '6', 'Compute Var[Y]': '2', 'Compute Cov[X,Y]': '0',
    'Compute E[XY]': '4'}

    problems = {first_prefix: first_problems, second_prefix: second_problems}
    random_prefix, random_questions = random.choice(list(problems.items()))
    random_question, random_answer = random.choice(list(random_questions.items()))
    await ctx.send(random_prefix + random_question)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content == random_answer:
        await ctx.send("Nice job!")
    else:
        await ctx.send("Oof! The correct answer is " + random_answer)

@bot.command(name="peq", help="Answer a point estimation question")
async def peq(ctx):
    a_i = random.randint(3, 6)
    b_i = random.randint(3, 6)
    c_i = random.randint(3, 6)
    d_i = random.randint(3, 6)
    e_i = random.randint(3, 6)
    problems = {'Consider X_1,...,X_5 with f(x;p)=pe^(-px^2), x>0, p>0. Find the MLE ' +
    f'estimator of p when x_1 = {a_i}, x_2 = {b_i}, x_3 = {c_i}, x_4 = {d_i}, x_5 = {e_i}':
    f'{round(5 / (a_i ** 2 + b_i ** 2 + c_i ** 2 + d_i ** 2 + e_i ** 2), 4)}',
    'Consider X_1,...,X_4 with f(x;t)=2(t^2)xe^((x^2)/t)(3^x), x>0, t>0. Find the MLE ' +
    f'estimator of t when x_1 = {a_i}, x_2 = {b_i}, x_3 = {c_i}, x_4 = {d_i}':
    f'{round((a_i ** 2 + b_i ** 2 + c_i ** 2 + d_i ** 2) / 8, 4)}',
    'Consider X_1,...,X_4 with f(x)=(2p-x)/(2p^2), 0<x<2p, p>0. Find the MOM ' +
    f'estimator of p when x_1 = {a_i}, x_2 = {b_i}, x_3 = {c_i}, x_4 = {d_i}':
    f'{3 * (a_i + b_i + c_i + d_i) / 8}',
    'Consider X_1,...,X_5 with f(x)=8(3t-4x)/(9t^2), 0<x<3t/4, t>0. Find the MOM ' +
    f'estimator of t when x_1 = {a_i}, x_2 = {b_i}, x_3 = {c_i}, x_4 = {d_i}, x_5 = {e_i}':
    f'{4 * (a_i + b_i + c_i + d_i + e_i) / 5}'}

    random_question, random_answer = random.choice(list(problems.items()))
    await ctx.send(random_question)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    if msg.content == random_answer:
        await ctx.send("Nice job!")
    else:
        await ctx.send("Oof! The correct answer is " + random_answer)

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)
