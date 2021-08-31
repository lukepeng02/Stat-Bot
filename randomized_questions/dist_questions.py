import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, DIST_QUESTIONS_LINES, extended_format

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

        'Let $X\sim N(&(d&), &(h&))$ and $Y\sim N(&(a&), &(b&))$. Let $C=&(j&)X+&(f&)Y\sim N(a,b)$. '
        'Find $ab$.=>&((j * d + f * a) * (j ** 2 * h + f ** 2 * b)&)':
        {'d': 'randint(16,25)', 'h': 'randint(20,40)', 'a': 'randint(10,20)',
        'f': 'randint(4,6)', 'b': 'randint(2,6)', 'j': 'randint(2,3)'},

        'While biking on Rainbow Road, Mario falls off according to a Poisson process at a rate ' +
        'of &(a&) times per lap. If a race is 3 laps, find the probability he falls &(b&) times ' +
        'in total.=>&(((3 * a) ** b) * exp(-3 * a) / factorial(b)&)':
        {'a': 'randuni(3.0, 4.0, 1)', 'b': 'randint(6,15)'},

        'While biking on Rainbow Road, Mario falls off according to a Poisson process at a rate ' +
        'of &(a&) times per lap. Find the variance in the number of laps it takes for him to fall ' +
        '&(b&) times.=>&(b / a ** 2&)':
        {'a': 'randuni(3.0,4.0,1)', 'b': 'randint(4,10)'},

        'Consider a random variable $X$ with pdf $f(x)=\\frac{{x}}{{&(a * (a + 1) / 2&)}}, x=' +
        '1,2,...,&(a&)$. Find $Var[X]$.=>&(a * (a + 1) / 2 - ((2 * a + 1) / 3) ** 2&)':
        {'a': 'randint(4,8)'},

        'Let the mgf of $X$ be $M_X(t)=0.2e^{{&(a&)t}}+0.2e^{{&(a-1&)t}}+0.3e^{{&(a-2&)t}}+' +
        '0.3e^{{&(a-3&)t}}$. Find $Var[X]$.=>1.21':
        {'a': 'randint(4,14)'},

        'Let the mgf of $X$ be $M_X(t)=\\frac{{&(p&)e^{{&(r&)t}}}}{{(1-&(1-p&)e^{{t}})^&(r&)}},' +
        't<-\\text{{ln}}(&(1-p&))$. Find $Var[X]$.=>&(r * (1 - p) / p ** 2&)':
        {'p': 'randuni(0.1,0.9,2)', 'r': 'randint(3,7)'},

        'Suppose the scores on a 50-point alchemy exam had pdf $f(x)=\\frac{{1}}{{2250}}(2x+5)$ ' +
        'and ranged between 20 and 50. If Harry scored &(a&), what percentile is he?=>' +
        '&((a ** 2 + 5 * a - 500) / 2250&)':
        {'a': 'randint(25,45)'},

        'Suppose the scores on a 50-point alchemy exam had pdf $f(x)=\\frac{{1}}{{2250}}(2x+5)$ ' +
        'and ranged between 20 and 50. If Harry scored in percentile &(a&), what was his score?=>' +
        '&((15 * sqrt(0.4 * a + 9) - 5) / 2&)':
        {'a': 'randint(5,90)'},

        'Let $X$ have pdf $f(x)=x^3-x+\\frac{{1}}{{2}}$ when $-1<x<1$. Find the percentile of &(a&).' +
        '=>&(a**4/4-a**2/2+a/2+3/4&)': {'a': 'randuni(-0.9,0.9,2)'},

        'Suppose $E[X]=&(a&)$. Find $E[&(b&)X+&(c&)]$.=>&(a*b+c&)':
        {'a': 'randint(25,50)', 'b': 'randint(10,20)', 'c': 'randint(1,200)'},

        'Suppose $Var[X]=&(a&)$. Find $Var[&(b&)X+&(c&)]$.=>&(a*b**2&)':
        {'a': 'randint(15,40)', 'b': 'randint(4,10)', 'c': 'randint(1,200)'},

        'Suppose the time it takes for customers to shop at Mall-mart follows an exponential ' +
        'distribution with mean &(t&) minutes. If &(b&) customers enter now, find the expected ' +
        'number of them left after &(c&) minutes.=>&(exp(-1 * c / t) * b&)':
        {'t': 'randint(30,40)', 'b': 'randint(20,30)', 'c': 'randint(40,50)'},

        'At a certain hospital, births occur according to a Poisson process with a rate of &(a&) ' +
        'per day. Find the probability none will occur within the next &(b&) minutes, if it is ' +
        'already known none will in the next &(c&) minutes.=>&(exp(-1*a*(b-c)/1440)&)':
        {'a': 'randint(15,25)', 'b': 'randint(60,120)', 'c': 'randint(30,40)'},

        'I roll a &(a&)-sided die until a 1 comes up. If I have already rolled &(b&) times, ' +
        'what the expected number of rolls I still need to make?=>&(a&)':
        {'a': 'randint(6,12)', 'b': 'randint(3,5)'},

        'Consider a random variable $X$ with pdf $f(x)=\\frac{{x}}{{&(a * (a + 1) / 2&)}}, x=' +
        '1,2,...,&(a&)$. Find $E[X^3]$.=>&((6*a**3+9*a**2+a-1)/15&)':
        {'a': 'randint(4,8)'},

        'Let $X\sim$ Gamma$(&(a&),&(t&))$. Find $E[X^2]$.=>&(t**2*(a**2+a)&)':
        {'a': 'randint(4,8)', 't': 'randint(3,10)'},

        'Let $X\sim$ B$(&(n&),&(p&))$. Find $E[(X+1)^2]$.=>&(n*p*(1-p)+(n*p)**2+2*n*p+1&)':
        {'n': 'randint(4,8)', 'p': 'randuni(0.02,0.98,2)'}, #25

        'Let the mgf of $X$ be $M_X(t)=e^{{&(m&)t+&(s/2&)t^2}},' +
        't\in (-\infty,\infty)$. Find $E[X^2]$.=>&(s+m**2&)':
        {'m': 'randint(2,5)', 's': 'randint(15,30)'},

        'Let $X$ have pdf $f(x)=-\\frac{{3}}{{4}}x^2+\\frac{{3}}{{2}}x$ in the interval ' +
        '$x\in [0,2]$. Find $P[X>&(a&)]$.=>&(a**3/4-3*a**2/4+1&)':
        {'a': 'randuni(0.1,1.9,1)'},

        'Consider $X \sim N(&(m&),&(s&))$ and $Y=&(a&)X+&(b&) \sim N(a,b)$. Find $ab$.' +
        '=>&((a*m+b)*(a**2*s)&)':
        {'m': 'randint(10,20)', 's': 'randint(5,10)', 'a': 'randint(3,7)', 'b': 'randint(10,20)'},

        'Suppose the time it takes for customers to shop at Mall-mart follows an exponential ' +
        'distribution with mean &(t&) minutes. Find the probability that a customer spends less than ' +
        '&(c&) minutes shopping.=>&(1-exp(-1 * c / t)&)':
        {'t': 'randint(30,40)', 'c': 'randint(40,50)'},

        'Suppose Albert tells his students to read the syllabus according to a ' +
        'Poisson distribution with mean &(l&) times per week. Find the probability he does so ' +
        '&(a&) times this week.=>&(l**a*exp(-1 * l)/factorial(a)&)':
        {'l': 'randint(5,10)', 'a': 'randint(2,12)'},
        }

hardcoded_problems = {}
for line in DIST_QUESTIONS_LINES:
    hardcoded_problems[line.split(' => ')[0]] = line.split(' => ')[1]

class Distributions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="distq", help="Answer a distribution question")
    async def distq(self, ctx):
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
    bot.add_cog(Distributions(bot))