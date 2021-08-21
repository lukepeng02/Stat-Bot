import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, extended_format

random_problems = {
        'Consider $X_1,...,X_5$ with pdf $f(x;\\theta)=\\frac{{1}}{{\\theta}}e^{{-\\frac{{x}}{{\\theta}}}}, ' +
        'x\geq0, \\theta>0$. Find the MLE estimator of $\\theta$ when $x_1 = &(a&), x_2 = &(b&), ' +
        'x_3 = &(c&), x_4 = &(d&), x_5 = &(e&)$=>&((a+b+c+d+e)/5&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)',
        'e': 'randint(3,6)'},

        'Consider $X_1,...,X_4$ with pdf $f(x;p)=p^{{-2}}xe^{{-x/p}}, x>0, p>0$. Find the MLE ' +
        'estimator of $p$ when $x_1 = &(a&), x_2 = &(b&), x_3 = &(c&), x_4 = &(d&)$' +
        '=>&((a+b+c+d) / 8&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)'},

        'Consider $X_1,...,X_5$ with pdf $f(x;\\theta)=2\\theta^2x^3e^{{-\\theta x^2}}, ' +
        'x>0, \\theta>0$. Find the MLE estimator of $\\theta$ when $x_1 = &(a&), x_2 = &(b&), ' +
        'x_3 = &(c&), x_4 = &(d&), x_5 = &(e&)$=>&(10/(a**2+b**2+c**2+d**2+e**2)&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)',
        'e': 'randint(3,6)'},

        'Consider $X$ whose pmf is listed as the following ordered pairs in the format $(x,f(x))$: ' +
        '$(0,3\\theta/5), (1,2\\theta/5), (2,3(1-\\theta)/5), (3,2(1-\\theta)/5)$, where ' +
        '$\\theta\in[0,1]$. Find the MLE estimator of $\\theta$ when a sample of size 10 has the ' +
        'following observed values: &(a&) 0(s), &(b&) 1(s), &(c&) 2(s), and &(10-a-b-c&) 3(s).' +
        '=>&((a+b)/10&)': {'a': 'randint(1,4)', 'b': 'randint(0,3)', 'c': 'randint(0,3)'},

        'Consider $X_1,...,X_4$ with pdf $f(x;p)=\\frac{{2p-x}}{{2p^2}}, 0<x<2p, p>0$. Find the MOM ' +
        'estimator of $p$ when $x_1 = &(a&), x_2 = &(b&), x_3 = &(c&), x_4 = &(d&)$' +
        '=>&(3 * (a + b + c + d) / 8&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)'},

        'Consider $X_1,...,X_5$ with pdf $f(x;t)=8\cdot\\frac{{3t-4x}}{{9t^2}}, 0<x<\\frac{{3t}}{{4}}, t>0$. ' +
        'Find the MOM estimator of $t$ when $x_1=&(a&), x_2=&(b&), x_3=&(c&), x_4=&(d&), x_5=&(e&)$' +
        '=>&(4 * (a + b + c + d + e) / 5&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)',
        'e': 'randint(3,6)'},

        'Consider $X_1,...,X_5$ with pdf $f(x;p)=8\cdot\\frac{{20p-8x}}{{25p^2}}, 0<x<\\frac{{5p}}{{2}}, p>0$. ' +
        'Find the MOM estimator of $p$ when $x_1=&(a&), x_2=&(b&), x_3=&(c&), x_4=&(d&), x_5=&(e&)$' +
        '=>&(6 / 5 * (a + b + c + d + e) / 5&)':
        {'a': 'randint(3,6)', 'b': 'randint(3,6)', 'c': 'randint(3,6)', 'd': 'randint(3,6)',
        'e': 'randint(3,6)'},

        'Consider $X$ whose pmf is listed as the following ordered pairs in the format $(x,f(x))$: ' +
        '$(0,3\\theta/5), (1,2\\theta/5), (2,3(1-\\theta)/5), (3,2(1-\\theta)/5)$, where ' +
        '$\\theta\in[0,1]$. Find the MLE estimator of $\\theta$ when a sample of size 10 has the ' +
        'following observed values: &(a&) 0(s), &(b&) 1(s), &(c&) 2(s), and &(10-a-b-c&) 3(s).' +
        '=>&((12-5*(b+2*c+3*(10-a-b-c))/10)/10&)'
        : {'a': 'randint(1,4)', 'b': 'randint(0,3)', 'c': 'randint(0,3)'},
        }


class Point_Estimation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="peq", help="Answer a point estimation question")
    async def peq(self, ctx):
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
    bot.add_cog(Point_Estimation(bot))