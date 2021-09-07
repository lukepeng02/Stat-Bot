import discord
import random
from sympy import *
from discord.ext import commands
from globals import BIVAR_QUESTIONS_LINES, extended_format, send_and_check

random_problems = {
        'Let $\sigma_X=&(a&), \sigma_Y=&(b&)$, and $Var[&(c&)X-&(d&)Y]=&(e&)$. Find $\\rho_{XY}$.' +
        '=>&((a**2*c**2+b**2*d**2-e)/(2*a*b*c*d)&)':
        {'a': 'randint(3,7)', 'b': 'randint(3,7)', 'c': 'randint(2,5)', 'd': 'randint(2,5)',
        'e': 'randint(60,100)'},

        'Let $\sigma_X=&(a&), \sigma_Y=&(b&)$, and $\\rho_{XY}=&(e&)$. Find $Var[&(c&)X-&(d&)Y]$.' +
        '=>&((a**2*c**2+b**2*d**2-2*a*b*c*d*e)&)':
        {'a': 'randint(3,7)', 'b': 'randint(3,7)', 'c': 'randint(2,5)', 'd': 'randint(2,5)',
        'e': 'randuni(0.01,0.99,2)'},
}

hardcoded_problems = {}
for line in BIVAR_QUESTIONS_LINES:
    hardcoded_problems[line.split(' => ')[0]] = line.split(' => ')[1]

class Bivariate_Distributions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bivarq", help="Answer a bivariate distribution question")
    async def bivarq(self, ctx):
        choice = random.randrange(5 * len(random_problems) + len(hardcoded_problems))
        formatted_question, formatted_answer = None, None
        if choice in range(5 * len(random_problems)):
            random_question, variables = random.choice(list(random_problems.items()))
            formatted_question, formatted_answer = extended_format(random_question, variables)
        else:
            formatted_question, formatted_answer = random.choice(list(hardcoded_problems.items()))

        await send_and_check(formatted_question, formatted_answer, self.bot, ctx)

def setup(bot):
    bot.add_cog(Bivariate_Distributions(bot))