import random
from sympy import *
from scipy import stats
from re import sub

COMMAND_LIST = ['!help', '!ansformat', '!probq', '!miscprobq', '!distq', '!bivarq', '!peq', '!ciq']

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
    expression = input
    def vars_to_nums():
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
        return new_dict

    new_dict = vars_to_nums()
    a = 0.05
    print(stats.t.ppf(a, 20))

    def substitute_regex(expression, reg, nums):
        subbed = expression
        while len(nums) > 0:
            subbed = sub(reg, str(nums[0]), subbed, 1)
            del nums[0]
        return subbed

    def sympify_stats(expression):
        if '@(' not in expression:
            return expression
        for index, char in enumerate(expression):
            if expression[index:index+7] == '@(tinv(':
                end_index = expression[index+1:].index('@)') + index

                first_expression = expression[index+7:end_index].split(",")[0]
                second_expression = expression[index+7:end_index].split(",")[1]

                first_value = float(round_if_needed(sympify(first_expression).subs(new_dict)))
                second_value = float(round_if_needed(sympify(second_expression).subs(new_dict)))

                t_stat = round(stats.t.ppf(first_value, second_value), 8)
                nums = [t_stat]
                expression = substitute_regex(expression, r'@\((.*?)@\)', nums)
                break

        return sympify_stats(expression)

    expression = sympify_stats(expression)

    def generate_special_indices():
        start_indices = []
        end_indices = []
        for index, char in enumerate(expression):
            if char == '&' and expression[index + 1] == '(':
                start_indices.append(index + 2)
            elif char == '&' and expression[index + 1] == ')':
                end_indices.append(index)
        return start_indices, end_indices

    start_indices, end_indices = generate_special_indices()

    def convert_sympy_to_nums(start_indices, end_indices):
        nums = []
        for start_index, end_index in zip(start_indices, end_indices):
            evaluated = sympify(expression[start_index:end_index]).subs(new_dict)
            nums.append(round_if_needed(evaluated))
        return nums

    nums = convert_sympy_to_nums(start_indices, end_indices)

    expression = substitute_regex(expression, r'&\((.*?)&\)', nums)

    return expression.split('=>')

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