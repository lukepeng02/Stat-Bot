import random
from sympy import *
from re import sub

COMMAND_LIST = ['!help', '!ansformat', '!probq', '!miscprobq', '!distq', '!bivarq', '!peq']

prob_questions = open("hardcoded/prob_questions.txt", 'r')
PROB_QUESTIONS_LINES = prob_questions.read().splitlines()
prob_questions.close()

misc_prob_questions = open("hardcoded/misc_prob_questions.txt", 'r')
MISC_PROB_QUESTIONS_LINES = misc_prob_questions.read().splitlines()
misc_prob_questions.close()

dist_questions = open("hardcoded/dist_questions.txt", 'r')
DIST_QUESTIONS_LINES = dist_questions.read().splitlines()
dist_questions.close()

bivar_questions = open("hardcoded/bivarq.txt", 'r')
BIVAR_QUESTIONS_LINES = bivar_questions.read().splitlines()
bivar_questions.close()

pe_questions = open("hardcoded/point_est_questions.txt", 'r')
PE_QUESTIONS_LINES = pe_questions.read().splitlines()
pe_questions.close()

def extended_format(input, vars):
    new_dict = {}
    for key, value in vars.items():
        to_add = value
        if value.startswith("randint"):
            ints = [int(i) for i in (value[8:len(value) - 1].split(","))]
            to_add = random.randint(ints[0], ints[1])
        elif value.startswith("randuni"):
            vals = value[8:len(value) - 1].split(",")
            to_add = round(random.uniform(float(vals[0]), float(vals[1])), int(vals[2]))
        new_dict[symbols(key)] = to_add

    start_indices = []
    end_indices = []
    for index, char in enumerate(input):
        if char == '&' and input[index + 1] == '(':
            start_indices.append(index + 2)
        elif char == '&' and input[index + 1] == ')':
            end_indices.append(index)

    nums = []
    for start_index, end_index in zip(start_indices, end_indices):
        evaluated = sympify(input[start_index:end_index]).subs(new_dict)
        nums.append(round_if_needed(evaluated))

    reg = r'&\((.*?)&\)'
    subbed = input
    while len(nums) > 0:
        subbed = sub(reg, str(nums[0]), subbed, 1)
        del nums[0]

    return subbed.split('=>')

def round_if_needed(val):
    def is_int(val):
        return round(val % 1, 10) == 0
    def digits_after_decimal(val):
        if '.' not in str(val):
            return
        return len(str(val).split('.')[1])

    if is_int(val):
        return round(val)
    elif digits_after_decimal(float(val)) <= 4:
        return float(val)
    else:
        return round(float(val), 4)