import discord
import random
from sympy import *
from discord.ext import commands
from globals import PE_QUESTIONS_LINES, extended_format, send_and_check

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
        '=>&((a+b)/10&)':
        {'a': 'randint(1,4)', 'b': 'randint(0,3)', 'c': 'randint(0,3)'},

        'Consider $X\sim N(&(a&),&(b&))$. Find the standard deviation of $\overline{{X}}$ when ' +
        '$n=$&(c&).=>&(sqrt(b/c)&)':
        {'a': 'randint(10,40)', 'b': 'randint(10,30)', 'c': 'randint(5,10)'},
        }

hardcoded_problems = {}
for line in PE_QUESTIONS_LINES:
    hardcoded_problems[line.split(' => ')[0]] = line.split(' => ')[1]

class Point_Estimation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="peq", help="Answer a sampling/point estimation question")
    async def peq(self, ctx):
        choice = random.randrange(2 * len(random_problems) + len(hardcoded_problems))
        formatted_question, formatted_answer = None, None
        if choice in range(2 * len(random_problems)):
            random_question, variables = random.choice(list(random_problems.items()))
            formatted_question, formatted_answer = extended_format(random_question, variables)
        else:
            formatted_question, formatted_answer = random.choice(list(hardcoded_problems.items()))

        await send_and_check(formatted_question, formatted_answer, self.bot, ctx)

def setup(bot):
    bot.add_cog(Point_Estimation(bot))