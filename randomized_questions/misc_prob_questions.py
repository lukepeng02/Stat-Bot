import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, MISC_PROB_QUESTIONS_LINES, extended_format


random_problems = {'I have &(f + s + t&) cards: &(f&) are red ' +
        'on both sides, &(s&) are blue on both sides, and &(t&) are blue on one ' +
        'side and red on the other. I choose a random card and see it is red on this side. ' +
        'What is the probability the other side is blue?=>&(t / (2 * f + t)&)':
        {'f': 'randint(2,6)', 's': 'randint(2,6)', 't': 'randint(2,6)'},

        'The probability David takes the bus on any day is &(f&), and the probability it ' +
        'rains on any day is &(s&). If the probability that it is not raining and David is ' +
        'not taking the bus is &(1 - f - s + t&), find the probability it ' +
        'is raining, given David is not taking the bus.=>&((s - t) / (1 - f)&)':
        {'f': 'randuni(0.5, 0.7, 2)', 's': 'randuni(0.5, 0.7, 2)',
        't': 'randuni(0.41, 0.5, 2)'},

        'Let the pmf of $X$ be $f(x)=c\cdot\\frac{{&(f&)^x}}{{x!}}, x = 3,4,5,...$ What is $c$?' +
        '=>&(2 / (2 * exp(f) - f ** 2 - 2 * f - 2)&)': {'f': 'randint(2,6)'},

        'I roll a fair six-sided die &(d&) times. What is $P$[exactly &(f&) perfect squares]?' +
        '=>&(binomial(d, f) * ((1 / 3) ** f) * ((2 / 3) ** (d - f))&)':
        {'d': 'randint(10,20)', 'f': 'randint(2,6)'},

        'I roll a fair &(e&)-sided die &(f&) times. What is the expected value for the product?' +
        '=>&(((e + 1) / 2) ** f&)': {'e': 'randint(6,10)', 'f': 'randint(2,6)'},
        
        'An ant starts at $(0,0)$ and can only go up by 1 or to the right by 1 each move. ' +
        'Find the probability it has visited $(&(a&),&(b&))$, given that it is at ' +
        '$(&(n&),&(k&))$=>&(binomial(a+b,a) * binomial(n+k-a-b,n-a) / binomial(n+k,n)&)':
        {'n': 'randint(5,10)', 'k': 'randint(5,10)', 'a': 'randint(1,4)', 'b': 'randint(1,4)'},
        
        'Let the pmf of $X$ be $f(x)=c\cdot\\frac{{&(a&)}}{{&(b&)^x}},x=1,2,...$ ' +
        'Determine the value of $c$=>&((b - 1) / a&)': {'a': 'randint(3,6)', 'b': 'randint(3,6)'},

        'Let the pmf of $X$ be $f(x)=c\cdot \\frac{{x+&(a&)}}{{&(b&)}}, x=0,1,...,5$. ' +
        'Determine the value of $c$=>&(b / (3 * (2 * a + 5))&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)'},

        'A giant hollow ball contains 50 urns: 20 Greek, 15 Japanese, 10 Chinese, and 5 Peruvian. ' +
        'If I choose 10 without replacement, find the probability I have &(a&) Greek, &(b&) Japanese, ' +
        '&(c&) Chinese, and &(10 - a - b - c&) Peruvian urns.=>&(binomial(20, a) * binomial(15, b) * ' +
        'binomial(10, c) * binomial(5, 10 - a - b - c) / binomial(50, 10)&)':
        {'a': 'randint(2,4)', 'b': 'randint(2,3)', 'c': 'randint(1,2)'},

        'Tom the Turkey lives in a coop with &(c&) other turkeys. This Thanksgiving season, &(b&) turkeys ' +
        'are randomly ``selected" every day and replaced with other turkeys. What is the probability ' +
        'Tom is ``selected" on day &(a&)?=>&((1 - b / (c + 1)) ** (a - 1) * (b / (c + 1))&)':
        {'a': 'randint(2,10)', 'b': 'randint(20,80)' ,'c': 'randint(249, 349)'},
        }

hardcoded_problems = {}
for line in MISC_PROB_QUESTIONS_LINES:
    hardcoded_problems[line.split(' => ')[0]] = line.split(' => ')[1]

class Misc_Probability(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="miscprobq", help="Answer a miscellaneous probability question")
    async def miscprobq(self, ctx):
        choice = random.randrange(2 * len(random_problems) + len(hardcoded_problems))
        formatted_question, formatted_answer = None, None
        if choice in range(2 * len(random_problems)):
            random_question, variables = random.choice(list(random_problems.items()))
            formatted_question, formatted_answer = extended_format(random_question, variables)
        else:
            formatted_question, formatted_answer = random.choice(list(hardcoded_problems.items()))

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
    bot.add_cog(Misc_Probability(bot))