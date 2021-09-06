import discord
import random
from sympy import *
from discord.ext import commands
from constants import COMMAND_LIST, extended_format

random_problems = {
        'In a sample of 30 students, the average number of calories eaten per day was &(100*a&). ' +
        'If it is known that the population standard deviation is &(10*b&) calories, ' +
        'find the lower confidence limit of a &(100-c&)$\%$ confidence interval for the population mean. ' +
        '(Assume it is normally distributed.)=>&(100*a+(@(norminv(c/200,0,1)@)*10*b/sqrt(30))&)':
        {'a': 'randint(15,25)', 'b': 'randint(15,25)', 'c': 'randint(2,10)'},

        'In a sample of 30 students, the average number of calories eaten per day was &(100*a&). ' +
        'If it is known that the population standard deviation is &(10*b&) calories, ' +
        'find the lower limit of a &(100-c&)$\%$ confidence lower bound for the population mean. ' +
        '(Assume it is normally distributed.)=>&(100*a+(@(norminv(c/100,0,1)@)*10*b/sqrt(30))&)':
        {'a': 'randint(15,25)', 'b': 'randint(15,25)', 'c': 'randint(2,10)'},

        'At Pirdew University, a sample of &(a&) students found the average IQ to be &(b&). ' +
        'If it is known that the population standard deviation is 16 IQ points, ' +
        'find the lower confidence limit of a &(100-c&)$\%$ confidence interval for the average ' +
        'student IQ at Pirdew. (Assume it is normally distributed.)' +
        '=>&(b+(@(norminv(c/200,0,1)@)*16/sqrt(a))&)':
        {'a': 'randint(50,75)', 'b': 'randint(85,105)', 'c': 'randint(2,10)'},

        'At Pirdew University, a sample of &(a&) students found the average IQ to be &(b&). ' +
        'If it is known that the population standard deviation is 16 IQ points, ' +
        'find the lower limit of a &(100-c&)$\%$ confidence lower bound for the average ' +
        'student IQ at Pirdew. (Assume it is normally distributed.)' +
        '=>&(b+(@(norminv(c/100,0,1)@)*16/sqrt(a))&)':
        {'a': 'randint(50,75)', 'b': 'randint(85,105)', 'c': 'randint(2,10)'},

        'A survey is taken at the local Sandwich Queen joint. &(a&) people participated, ' +
        'and it was found the average weight was &(b&) pounds. If it is known that the population ' +
        'standard deviation at this location is &(d&) pounds, find the upper confidence limit of a ' +
        '&(100-c&)$\%$ confidence interval for the average weight of a customer there. ' +
        '(Assume it is normally distributed.)=>&(b-(@(norminv(c/200,0,1)@)*d/sqrt(a))&)':
        {'a': 'randint(50,75)', 'b': 'randint(175,195)', 'c': 'randint(2,10)', 'd': 'randint(40,50)'},

        '&(a&) pieces of popcorn are taken from a bag, and the amount of time it took for each ' +
        'to pop is measured (somehow). Suppose the mean time is &(b&) minutes. It is also known ' +
        'the standard deviation is 15 seconds. Find the upper confidence limit of a ' +
        '&(100-c&)$\%$ confidence interval for the average number of minutes it takes for a kernel ' +
        'to pop. (Assume it is normally distributed.) =>&(b-(@(norminv(c/200,0,1)@)*0.25/sqrt(a))&)':
        {'a': 'randint(40,70)', 'b': 'randuni(1.5,2.5,1)', 'c': 'randint(2,10)'},

        'Luke collects data on the number of hours his neighbors spend partying loudly ' +
        'per day. Suppose the sample size is &(a&) days, with mean &(b&) hours and standard ' +
        'deviation 1 hour. Find the upper confidence limit of a &(100-c&)$\%$ confidence ' +
        'interval for the average number of hours. (Assume it is normally distributed.)' +
        '=>&(b-(@(tinv(c/200,a-1)@)/sqrt(a))&)':
        {'a': 'randint(5,10)', 'b': 'randuni(5,6,1)', 'c': 'randint(2,10)'},

        'Luke collects data on the number of hours his neighbors spend partying loudly ' +
        'per day. Suppose the sample size is &(a&) days, with mean &(b&) hours and standard ' +
        'deviation 1 hour. Find the upper limit of a &(100-c&)$\%$ confidence ' +
        'upper bound for the average number of hours. (Assume it is normally distributed.)' +
        '=>&(b-(@(tinv(c/100,a-1)@)/sqrt(a))&)':
        {'a': 'randint(5,10)', 'b': 'randuni(5,6,1)', 'c': 'randint(2,10)'},

        'For &(a&) days, Charlie produces an average of &(b&) ponds of chocolate per day, with ' +
        'a standard deviation of &(d&) pounds. Find the upper confidence limit of a ' +
        '&(100-c&)$\%$ confidence interval for the number of pounds of chocolate Charlie produces ' +
        'on average per day. (Assume it is normally distributed.)=>&(b-(@(tinv(c/200,a-1)@)*d/sqrt(a))&)':
        {'a': 'randint(20,30)', 'b': 'randint(60,70)', 'c': 'randint(2,10)', 'd': 'randint(4,8)'},

        'For &(a&) days, Charlie produces an average of &(b&) ponds of chocolate per day, with ' +
        'a standard deviation of &(d&) pounds. Find the upper limit of a ' +
        '&(100-c&)$\%$ confidence upper bound for the number of pounds of chocolate Charlie produces ' +
        'on average per day. (Assume it is normally distributed.)=>&(b-(@(tinv(c/100,a-1)@)*d/sqrt(a))&)':
        {'a': 'randint(20,30)', 'b': 'randint(60,70)', 'c': 'randint(2,10)', 'd': 'randint(4,8)'},

        'A survey of &(a&) people is conducted at the Blue Tiger bar on a Friday night. ' +
        'Suppose the average number of drinks per person is &(b&) and the standard deviation ' +
        'is 2. Find the upper confidence limit of a &(100-c&)$\%$ confidence interval for ' +
        'the number of drinks per person on a Friday night here. (Assume it is normally distributed.)' +
        '=>&(b-(@(tinv(c/200,a-1)@)*2/sqrt(a))&)':
        {'a': 'randint(20,30)', 'b': 'randint(7,13)', 'c': 'randint(2,10)'},

        'In &(a&) days, Michael Phelps consumed an average of &(100*b&) calories, with a standard ' +
        'deviation of &(100*d&). Find the lower confidence limit of a &(100-c&)$\%$ confidence interval ' +
        'for the average number of calories he consumes per day. (Assume it is normally distributed.)' +
        '=>&(100*b+(@(tinv(c/200,a-1)@)*100*d/sqrt(a))&)':
        {'a': 'randint(10,20)', 'b': 'randint(95,125)', 'c': 'randint(2,10)', 'd': 'randint(3,8)'},

        'A survey of &(a&) ``fans" of Enlightenment (a famous grunge band) was conducted. ' +
        'It was discovered that &(b&) of the participants had only heard of their signature song, ' +
        '``Reeks of Juvenile Sweat". Find the upper confidence limit of a &(100-c&)$\%$ confidence ' +
        'interval for the proportion of all Enlightenment ``fans" who only know their signature song.' +
        '=>&(b/a-(@(norminv(c/200,0,1)@)*sqrt((b/a*(1-b/a)/a)))&)':
        {'a': 'randint(150,200)', 'b': 'randint(100,130)', 'c': 'randint(2,10)'},

        'A survey of &(a&) ``fans" of Enlightenment (a famous grunge band) was conducted. ' +
        'It was discovered that &(b&) of the participants had only heard of their signature song, ' +
        '``Reeks of Juvenile Sweat". Find the upper limit of a &(100-c&)$\%$ confidence ' +
        'upper bound for the proportion of all Enlightenment ``fans" who only know their signature song.' +
        '=>&(b/a-(@(norminv(c/100,0,1)@)*sqrt((b/a*(1-b/a)/a)))&)':
        {'a': 'randint(150,200)', 'b': 'randint(100,130)', 'c': 'randint(2,10)'},

        'A survey of &(a&) FAR residents was conducted. In response to the yes/no question, ' +
        '``Do you like it here?", &(b&) of the participants responded with ``no". Find the upper ' +
        'confidence limit of a &(100-c&)$\%$ confidence interval for the proportion of all FAR ' +
        'residents who do not enjoy living there.' +
        '=>&(b/a-(@(norminv(c/200,0,1)@)*sqrt((b/a*(1-b/a)/a)))&)':
        {'a': 'randint(150,200)', 'b': 'randint(100,130)', 'c': 'randint(2,10)'},

        'A survey of &(a&) FAR residents was conducted. In response to the yes/no question, ' +
        '``Do you like it here?", &(b&) of the participants responded with ``no". Find the upper ' +
        'limit of a &(100-c&)$\%$ confidence upper bound for the proportion of all FAR ' +
        'residents who do not enjoy living there.' +
        '=>&(b/a-(@(norminv(c/100,0,1)@)*sqrt((b/a*(1-b/a)/a)))&)':
        {'a': 'randint(150,200)', 'b': 'randint(100,130)', 'c': 'randint(2,10)'},

        'A survey of &(a&) Americans was conducted. It was discovered that &(b&) of the ' +
        'responders had received at least one dose of a COVID vaccine. Find the lower ' +
        'confidence limit of a &(100-c&)$\%$ confidence interval for the proportion of all Americans ' +
        'who have received at least one dose.' +
        '=>&(b/a+(@(norminv(c/200,0,1)@)*sqrt((b/a*(1-b/a)/a)))&)':
        {'a': 'randint(1500,2000)', 'b': 'randint(1000,1300)', 'c': 'randint(2,10)'},

        'A survey of &(a&) U of I students was conducted. It was discovered that &(b&) of the ' +
        'responders pronounce ``syrup" like ``SEER-up" (aka the correct way), while the rest pronounce ' +
        'it ``SIR-up". Find the upper confidence limit of a &(100-c&)$\%$ confidence interval for the ' +
        'proportion of all U of I students who pronounce ``syrup" \\textit{{correctly}}.' +
        '=>&(b/a-(@(norminv(c/200,0,1)@)*sqrt((b/a*(1-b/a)/a)))&)':
        {'a': 'randint(150,200)', 'b': 'randint(85,115)', 'c': 'randint(2,10)'},

        'At a water bottling plant, WALL-E fills 500-mL bottles. If a sample of &(a&) bottles ' +
        'is collected and the variance is found to be &(b&) mL$^2$, find the upper confidence limit ' +
        'of a &(100-c&)$\%$ confidence interval for the variance of bottle filling.' +
        '=>&((a-1)*b/@(chiinv(c/200,a-1)@)&)':
        {'a': 'randint(50,70)', 'b': 'randuni(1.0,2.5,1)', 'c': 'randint(2,10)'},

        'At a water bottling plant, WALL-E fills 500-mL bottles. If a sample of &(a&) bottles ' +
        'is collected and the variance is found to be &(b&) mL$^2$, find the upper limit ' +
        'of a &(100-c&)$\%$ confidence upper bound for the variance of bottle filling.' +
        '=>&((a-1)*b/@(chiinv(c/100,a-1)@)&)':
        {'a': 'randint(50,70)', 'b': 'randuni(1.0,2.5,1)', 'c': 'randint(2,10)'},

        'To practice for the school archery team tryouts, Katniss shoots &(a&) arrows at a target. ' +
        'The variance of the distance to the center is &(b&) in.$^2$. Find the lower confidence limit ' +
        'of a &(100-c&)$\%$ confidence interval for the true variance.' +
        '=>&((a-1)*b/@(chiinv(1-c/200,a-1)@)&)':
        {'a': 'randint(20,30)', 'b': 'randuni(2.0,3.0,1)', 'c': 'randint(2,10)'},

        'Suppose Eli\'s Electronics manufactures thermostats. On inspection day, a manager randomly ' +
        'tests &(a&) products and measures the difference between the observed and expected ' +
        'temperatures, resulting in a variance of &(b&) $^{\circ}$F$^2$. Find the lower confidence ' +
        'limit of a &(100-c&)$\%$ confidence interval for the true standard deviation.' +
        '=>&(sqrt((a-1)*b/@(chiinv(1-c/200,a-1)@))&)':
        {'a': 'randint(20,30)', 'b': 'randuni(0.5,1.0,1)', 'c': 'randint(2,10)'},

        'Suppose Eli\'s Electronics manufactures thermostats. On inspection day, a manager randomly ' +
        'tests &(a&) products and measures the difference between the observed and expected ' +
        'temperatures, resulting in a variance of &(b&) $^{\circ}$F$^2$. Find the lower ' +
        'limit of a &(100-c&)$\%$ confidence lower bound for the true standard deviation.' +
        '=>&(sqrt((a-1)*b/@(chiinv(1-c/100,a-1)@))&)':
        {'a': 'randint(20,30)', 'b': 'randuni(0.5,1.0,1)', 'c': 'randint(2,10)'},

        'Suppose Chloe hoards treats and gambles them with the other dogs on the block every week. ' +
        'In the past &(a&) weeks, the variance of her winnings (and losses) was &(b&) treats$^2$. ' +
        'Find the upper confidence limit of a &(100-c&)$\%$ confidence interval for the true standard ' +
        'deviation.=>&(sqrt((a-1)*b/@(chiinv(c/200,a-1)@))&)':
        {'a': 'randint(5,10)', 'b': 'randuni(3.0,4.0,1)', 'c': 'randint(2,10)'},

        'A survey of &(a&) males (pop.1) and &(b&) females (pop.2) is conducted. On average, male ' +
        'responders played video games for &(d&) minutes per day, compared to &(e&) for females. If it ' +
        'is known the population standard deviation is &(f&) minutes for males and &(g&) for females, ' +
        'find the upper confidence limit of a &(100-c&)$\%$ confidence interval for the true difference ' +
        'in average number of minutes per day between the two groups.' +
        '=>&((d-e)-@(norminv(c/200,0,1)@)*sqrt(f**2/a+g**2/b)&)':
        {'a': 'randint(100,200)', 'b': 'randint(100,200)', 'c': 'randint(2,10)', 'd': 'randint(300,360)',
        'e': 'randint(30,60)', 'f': 'randint(100,120)', 'g': 'randint(10,20)'},

        'A survey of &(a&) males (pop.1) and &(b&) females (pop.2) is conducted. On average, male ' +
        'responders ate &(100*d&) calories per day, compared to &(100*e&) for females. If it ' +
        'is known the population standard deviation is &(10*f&) calories for males and &(10*g&) for ' +
        'females, find the lower confidence limit of a &(100-c&)$\%$ confidence interval for the true ' +
        'difference in average calories eaten per day between the two groups.' +
        '=>&((100*(d-e))+@(norminv(c/200,0,1)@)*sqrt(100*(f**2/a+g**2/b))&)':
        {'a': 'randint(100,200)', 'b': 'randint(100,200)', 'c': 'randint(2,10)', 'd': 'randint(23,28)',
        'e': 'randint(18,22)', 'f': 'randint(23,28)', 'g': 'randint(18,22)'},

        'A survey of &(a&) students from Albert\'s class (pop.1) and &(b&) students from Bob\'s class ' +
        '(pop.2) is conducted. On average, Albert\'s students spent &(d&) hours on homework per week, ' +
        'compared to &(e&) for Bob\'s. Samples 1 and 2 had a standard deviation of &(f&) and &(g&) ' +
        'hours, respectively. Assume the population standard deviation is the same for both classes. ' +
        'Find the upper confidence limit of a &(100-c&)$\%$ confidence interval for the true ' +
        'difference in average calories eaten per day between the two groups.' +
        '=>&((d-e)-@(tinv(c/200,a+b-2)@)*sqrt((1/a+1/b)*((a-1)*f**2+(b-1)*g**2)/(a+b-2))&)':
        {'a': 'randint(30,40)', 'b': 'randint(30,40)', 'c': 'randint(2,10)', 'd': 'randuni(2.0,3.0,1)',
        'e': 'randuni(3.5,4.5,1)', 'f': 'randuni(0.5,1.0,1)', 'g': 'randuni(0.6,1.2,1)'},

        'A survey of &(a&) Stats majors (pop.1) and &(b&) non-Stats majors (pop.2) is conducted. ' +
        'On average, Stats majors received a &(d&) in Stat 400, compared to &(e&) for non-Stats ' +
        'majors. Samples 1 and 2 had a standard deviation of &(f&) and &(g&), respectively. Assume ' +
        'the population standard deviation is the same for both classes. ' +
        'Find the lower confidence limit of a &(100-c&)$\%$ confidence interval for the true ' +
        'difference in the average grade received in Stat 400 between the two groups.' +
        '=>&((d-e)+@(tinv(c/200,a+b-2)@)*sqrt((1/a+1/b)*((a-1)*f**2+(b-1)*g**2)/(a+b-2))&)':
        {'a': 'randint(30,40)', 'b': 'randint(30,40)', 'c': 'randint(2,10)', 'd': 'randint(95,98)',
        'e': 'randint(91,93)', 'f': 'randuni(0.5,1.0,1)', 'g': 'randuni(0.5,1.0,1)'},

        'Chloe (pop.1) and Zoe (pop.2) have an asynchronous eating contest. In &(a&) sessions, Chloe ' +
        'eats an average of &(d&) treats, compared to Zoe\'s average of &(e&) treats in &(b&) sessions. ' +
        'Chloe has a sample standard deviation of &(f&), and Zoe has one of &(g&). Assume the population ' +
        'standard deviations are unequal. Find the lower confidence limit of a &(100-c&)$\%$ confidence ' +
        'interval for the true difference in the average number of treats eaten per session.' +
        '=>&((d-e)+@(tinv(c/200,floor((f**2/a+g**2/b)**2/((f**2/a)**2/(a-1)+(g**2/b)**2/(b-1))))@)*' +
        'sqrt(f**2/a+g**2/b)&)':
        {'a': 'randint(6,10)', 'b': 'randint(6,10)', 'c': 'randint(2,10)', 'd': 'randint(40,50)',
        'e': 'randint(35,45)', 'f': 'randint(5,8)', 'g': 'randint(4,8)'},

        '&(a&) males (pop.1) and &(b&) females (pop.2) responded to a survey. It was discovered that ' +
        'in the shower, males spent an average of &(d&) minutes, compared to &(e&) for females. Males ' +
        'had a sample standard deviation of &(f&) minutes, and females had one of &(g&). Assume the ' +
        'population standard deviations are unequal. Find the upper confidence limit of a &(100-c&)$\%$ ' +
        'confidence interval for the true difference in the average number of minutes spent in the shower.' +
        '=>&((d-e)-@(tinv(c/200,floor((f**2/a+g**2/b)**2/((f**2/a)**2/(a-1)+(g**2/b)**2/(b-1))))@)*' +
        'sqrt(f**2/a+g**2/b)&)':
        {'a': 'randint(30,40)', 'b': 'randint(40,50)', 'c': 'randint(2,10)', 'd': 'randint(5,15)',
        'e': 'randint(20,30)', 'f': 'randint(2,4)', 'g': 'randint(4,8)'},

        '&(a&) male-female couples were asked, "How many annoying habits does your significant ' +
        'other have?" For each couple, the difference in the male\'s response and the female\'s ' +
        'response was recorded. The average was &(b&) habits, and the standard ' +
        'deviation was &(d&). Find the lower confidence limit of a &(100-c&)$\%$ confidence interval ' +
        'for the true average difference in the number of bad habits across all male-female couples.' +
        '=>&(b+@(tinv(c/200,a-1)@)*d/sqrt(a)&)':
        {'a': 'randint(30,40)', 'b': 'randint(-10,-2)', 'c': 'randint(2,10)', 'd': 'randint(3,5)'},

        '&(a&) people have their IQ recorded before their very first day of classes at Pirdew ' +
        'University. After graduating, this figure is tested again. The average change in IQ was &(b&), ' +
        'and the standard deviation of the changes was &(d&). Find the lower confidence limit of ' +
        'a &(100-c&)$\%$ confidence interval for the mean change in IQ for all Pirdew students.' +
        '=>&(b+@(tinv(c/200,a-1)@)*d/sqrt(a)&)':
        {'a': 'randint(30,40)', 'b': 'randint(-30,-20)', 'c': 'randint(2,10)', 'd': 'randint(4,6)'},

        'To test the efficacy of a new fertilizer, Old MacDonald grows &(a&) carrots with the old ' +
        'fertilizer (pop.1) and &(b&) with the new one (pop.2). A few months later, he finds that &(d&) ' +
        'carrots from pop.1 and &(e&) from pop.2 measured at least 6 inches. Find the upper confidence ' +
        'limit of a &(100-c&)$\%$ confidence interval for the true difference in proportions, of carrots ' +
        'that are at least 6 inches long, between the two groups.=>&((d/a-e/b)-@(norminv(c/200,0,1)@)*' +
        'sqrt((a-d)*d/a**3+(b-e)*e/b**3)&)':
        {'a': 'randint(60,80)', 'b': 'randint(60,80)', 'c': 'randint(2,10)', 'd': 'randint(30,40)',
        'e': 'randint(45,55)'},

        '&(a&) males (pop.1) and &(b&) females (pop.2) were asked whether they liked black licorice. &(d&) ' +
        'males and &(e&) females responded ``yes". Find the lower confidence limit of a &(100-c&)$\%$ ' +
        'confidence interval for the true difference in proportions, of people who enjoy black licorice, ' +
        'between the two groups.=>&((d/a-e/b)+@(norminv(c/200,0,1)@)* sqrt((a-d)*d/a**3+(b-e)*e/b**3)&)':
        {'a': 'randint(40,60)', 'b': 'randint(30,50)', 'c': 'randint(2,10)', 'd': 'randint(5,15)',
        'e': 'randint(0,10)'},

        'Ash wants to form a &(100-c&)$\%$ confidence interval with width &(a&) pound(s) for the ' +
        'average weight of a Snorlax. If the Pokédex claims the population standard deviation ' +
        'is &(b&) pounds, find the appropriate sample size of this study.' +
        '=>&(ceiling((b*@(norminv(1-c/200,0,1)@)/a)**2)&)':
        {'a': 'randuni(0.5,1,1)', 'b': 'randint(10,20)', 'c': 'randint(2,10)'},
        }

class Confidence_Intervals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ciq", help="Answer a confidence interval question")
    async def ciq(self, ctx):
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
    bot.add_cog(Confidence_Intervals(bot))