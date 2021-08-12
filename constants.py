COMMAND_LIST = ['!help', '!ansformat', '!probq', '!miscprobq', '!distq', '!bivarq', '!peq']

prob_questions = open("hardcoded/prob_questions.txt", 'r')
PROB_QUESTIONS_LINES = prob_questions.read().splitlines()
prob_questions.close()

misc_prob_questions = open("hardcoded/misc_prob_questions.txt", 'r')
MISC_PROB_QUESTIONS_LINES = misc_prob_questions.read().splitlines()
misc_prob_questions.close()

bivar_questions = open("hardcoded/bivarq.txt", 'r')
BIVAR_QUESTIONS_LINES = bivar_questions.read().splitlines()
bivar_questions.close()