import discord
import random
from sympy import *
from discord.ext import commands
from globals import DELETE_EMOJI, extended_format, send_and_check

random_problems = {
        'Steve believes he can dig out an average 70-block high chunk down to bedrock level in &(a&) ' +
        'minutes. His friend Alex does not believe this, so she makes him mine &(b&) of these. ' +
        'If the average time is &(c&) minutes and the standard deviation is &(d&) minutes, determine ' +
        'the p-value of this test.' +
        '=>&(2*(1-@(tcdf((c-a)/(d/sqrt(b)),b-1)@))&)':
        {'a': 'randuni(39,41,1)', 'b': 'randint(7,10)', 'c': 'randuni(42,44,1)',
        'd': 'randuni(2,4,1)'},

        'Steve believes he can dig out an average 70-block high chunk down to bedrock level in &(a&) ' +
        'minutes. His friend Alex does not believe this, so she makes him mine &(b&) of these. ' +
        'The average time is &(c&) minutes and the standard deviation is &(d&) minutes. If $\\alpha$ ' +
        'is &(e&), determine the difference between the test statistic and positive critical value ' +
        'of this test.' +
        ' (This will be positive if $H_0$ is rejected.)=>&((c-a)/(d/sqrt(b))-@(tinv(1-e/2,b-1)@)&)':
        {'a': 'randuni(39,41,1)', 'b': 'randint(7,10)', 'c': 'randuni(42,44,1)',
        'd': 'randuni(2,4,1)', 'e': 'randuni(0.02,0.08,2)'},

        'Mario believes he can complete a lap of Rainbow Road in &(a&) seconds on average, but Luigi ' +
        'insists it will take longer. To test, Mario completes &(b&) laps with an average time of ' +
        '&(c&) seconds and standard deviation of &(d&) seconds. If $\\alpha$ is &(e&), determine the ' +
        'difference between the test statistic and critical value of this test.' +
        '=>&((c-a)/(d/sqrt(b))-@(tinv(1-e,b-1)@)&)':
        {'a': 'randint(60,70)', 'b': 'randint(5,8)', 'c': 'randint(65,75)',
        'd': 'randint(5,10)', 'e': 'randuni(0.02,0.08,2)'},

        'Mario believes he can complete a lap of Rainbow Road in &(a&) seconds on average, but Luigi ' +
        'insists it will take longer. To test, Mario completes &(b&) laps with an average time of ' +
        '&(c&) seconds and standard deviation of &(d&) seconds. Find the p-value of this test.' +
        '=>&(1-@(tcdf((c-a)/(d/sqrt(b)),b-1)@)&)':
        {'a': 'randint(60,70)', 'b': 'randint(5,8)', 'c': 'randint(65,75)',
        'd': 'randint(5,10)', 'e': 'randuni(0.02,0.08,2)'},
        
        'Sandwich Queen claims its stores in the country Burgerland earn an average of \$&(1000*a&) in ' +
        'revenue per month, with a standard deviation of \$&(100*d&). You think the real figure is higher, ' +
        'so you collect sales data on &(b&) stores. The average revenue in your sample is \$&(1000*c&). ' +
        'Determine the p-value of this test.=>&(1-@(normcdf(1000*(c-a)/(100*d/sqrt(b)))@)&)':
        {'a': 'randint(43,45)', 'b': 'randint(15,20)', 'c': 'randint(40,42)',
        'd': 'randint(80,90)'},

        'Sandwich Queen claims its stores in the country Burgerland earn an average of \$&(1000*a&) in ' +
        'revenue per month, with a standard deviation of \$&(100*d&). You think the real figure is higher, ' +
        'so you collect sales data on &(b&) stores. The average revenue in your sample is \$&(1000*c&). ' +
        'If $\\alpha$ is &(e&), determine the difference between the test statistic and ' +
        'critical value of this test. (Hint: it is negative)' +
        '=>&(1000*(c-a)/(100*d/sqrt(b))-@(norminv(1-e,0,1)@)&)':
        {'a': 'randint(43,45)', 'b': 'randint(15,20)', 'c': 'randint(40,42)',
        'd': 'randint(80,90)', 'e': 'randuni(0.02,0.08,2)'},

        'A giant peach orchard claims its peaches are normally distributed with a mean weight of &(a&) ' +
        'pounds, and a standard deviation of &(d&) pounds. James thinks the real figure is lower, ' +
        'so he picks &(b&) peaches. The average weight in his sample is &(c&) pounds. ' +
        'Determine the p-value of this test.=>&(@(normcdf((c-a)/(d/sqrt(b)))@)&)':
        {'a': 'randuni(11,13,1)', 'b': 'randint(5,8)', 'c': 'randuni(11,13,1)',
        'd': 'randuni(1.5,2.5,1)', 'e': 'randuni(0.02,0.08,2)'},

        'A giant peach orchard claims its peaches are normally distributed with a mean weight of &(a&) ' +
        'pounds, and a standard deviation of &(d&) pounds. James thinks the real figure is lower, ' +
        'so he picks &(b&) peaches. The average weight in his sample is &(c&) pounds. ' +
        'If $\\alpha$ is &(e&), determine the difference between the test statistic and ' +
        'critical value of this test.=>&((c-a)/(d/sqrt(b))-@(norminv(e,0,1)@)&)':
        {'a': 'randuni(11,13,1)', 'b': 'randint(5,8)', 'c': 'randuni(11,13,1)',
        'd': 'randuni(1.5,2.5,1)', 'e': 'randuni(0.02,0.08,2)'},

        'A website claims &(a&)\% of people are left-handed. Bob does not believe this, so he surveys ' +
        '&(b&) people and finds that &(c&) of them are left-handed. Compute the p-value of this test.' +
        '=>&(2*(0.5-Abs(0.5-@(normcdf((c/b-a/100)/sqrt((a/100)*(1-a/100)/b))@)))&)':
        {'a': 'randuni(9,11,1)', 'b': 'randint(55,60)', 'c': 'randint(4,8)'},

        'A website claims &(a&)\% of people are left-handed. Bob does not believe this, so he surveys ' +
        '&(b&) people and finds that &(c&) of them are left-handed. If $\\alpha$ is &(e&), determine ' +
        'the difference between the test statistic and negative critical value of this test.' +
        '=>&((c/b-a/100)/sqrt((a/100)*(1-a/100)/b)-@(norminv(e/2,0,1)@)&)':
        {'a': 'randuni(9,11,1)', 'b': 'randint(55,60)', 'c': 'randint(4,8)', 'e': 'randuni(0.02,0.08,2)'},

        'The manager of a lightsaber factory tells Luke &(a&)\% of all lightsabers produced are defective. ' +
        'Luke believes the real proportion is smaller, so he samples &(b&) of them and finds that &(c&) ' +
        'are defective. Compute the p-value of this test.' +
        '=>&(@(normcdf((c/b-a/100)/sqrt((a/100)*(1-a/100)/b))@)&)':
        {'a': 'randuni(8,10,1)', 'b': 'randint(70,100)', 'c': 'randint(5,10)'},
        
        'The manager of a lightsaber factory tells Luke &(a&)\% of all lightsabers produced are defective. ' +
        'Luke believes the real proportion is smaller, so he samples &(b&) of them and finds that &(c&) ' +
        'are defective. If $\\alpha$ is &(e&), determine the difference between the test statistic and ' +
        'critical value of this test. (This will be negative if $H_0$ is rejected.)' +
        '=>&((c/b-a/100)/sqrt((a/100)*(1-a/100)/b)-@(norminv(e,0,1)@)&)':
        {'a': 'randuni(8,10,1)', 'b': 'randint(70,100)', 'c': 'randint(5,10)', 'e': 'randuni(0.02,0.08,2)'},

        'Katniss claims she can shoot arrows such that the standard deviation of their ' +
        'distances to the center of a target is &(a&) inches. To win her love, Peeta assures her the ' +
        'real standard deviation is lower, so she shoots &(b&) arrows and finds that the sample ' +
        'standard deviation is &(c&) inches. Compute the p-value ' +
        'of this test.=>&(@(chicdf((b-1)*c**2/a**2,b-1)@)&)':
        {'a': 'randuni(3,4,2)', 'b': 'randint(10,15)', 'c': 'randuni(2.5,3.5,2)'},

        'Katniss claims she can shoot arrows such that the standard deviation of their ' +
        'distances to the center of a target is &(a&) inches. To win her love, Peeta assures her the ' +
        'real standard deviation is lower, so she shoots &(b&) arrows and finds that the sample ' +
        'standard deviation is &(c&) inches. If $\\alpha$ is &(e&), find the difference between the ' +
        'test statistic and critical value.=>&((b-1)*c**2/a**2 - @(chiinv(e,b-1)@)&)':
        {'a': 'randuni(3,4,2)', 'b': 'randint(10,15)', 'c': 'randuni(2.5,3.5,2)',
        'e': 'randuni(0.02,0.08,2)'},

        'The engineer of potato cuber brags his creation is so precise, it can cut potatoes into chunks ' +
        'with a variance of no more than &(a&) grams$^2$. His main rival believes this is baloney, so he ' +
        'measures the mass of &(b&) chunks. The sample variance turns out to be &(c&) grams$^2$. Find ' +
        'the p-value of this test.=>&(1-@(chicdf((b-1)*c/a,b-1)@)&)':
        {'a': 'randuni(2,2.5,2)', 'b': 'randint(20,30)', 'c': 'randuni(1.5,2,2)'},

        'The engineer of potato cuber brags his creation is so precise, it can cut potatoes into chunks ' +
        'with a variance of no more than &(a&) grams$^2$. His main rival believes this is baloney, so he ' +
        'measures the mass of &(b&) chunks. The sample variance turns out to be &(c&) grams$^2$. If ' +
        '$\\alpha$ is &(e&), find the difference between the test statistic and ' +
        'critical value.=>&((b-1)*c/a - @(chiinv(1-e,b-1)@)&)':
        {'a': 'randuni(2,2.5,2)', 'b': 'randint(20,30)', 'c': 'randuni(1.5,2,2)',
        'e': 'randuni(0.02,0.08,2)'},

        'The creator of the newest protein shake fad diet claims her users have lost 10\% of their body ' +
        'weight, with a standard deviation of &(a&)\%. To see whether the reported standard deviation is ' +
        'accurate, you survey &(b&) dieters. The sample standard deviation is &(c&)\%. Find the ' +
        'p-value of this test.=>&(2*(1-@(chicdf((b-1)*c**2/a**2,b-1)@))&)':
        {'a': 'randuni(1,2,2)', 'b': 'randint(10,15)', 'c': 'randuni(2.2,3.2,2)'},

        'The creator of the newest protein shake fad diet claims her users have lost 10\% of their body ' +
        'weight, with a standard deviation of &(a&)\%. To see whether the reported standard deviation ' +
        'is accurate, you survey &(b&) dieters. The sample standard deviation is &(c&)\%. If $\\alpha$ ' +
        'is &(e&), find the difference between the test statistic and larger critical value.' +
        '=>&((b-1)*c**2/a**2 - @(chiinv(1-e,b-1)@)&)':
        {'a': 'randuni(1,2,2)', 'b': 'randint(10,15)', 'c': 'randuni(2.2,3.2,2)',
        'e': 'randuni(0.02,0.08,2)'},

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