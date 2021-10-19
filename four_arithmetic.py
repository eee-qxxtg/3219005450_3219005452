# -*- coding = utf-8 -*-
# @Time : 2021/10/16 22:59
# @Author : eee
# @File : four_arithmetic.py
# @Software : PyCharm
from random import randint

exercises_num = 20  # 生成题目的个数
value_max = 10  # 题目中数值（自然数、真分数和真分数分母）的最大值


# 树的节点类
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.lchild = None
        self.rchild = None
        if value in ['+', '-', '*', '/']:
            self.result = None
        else:
            self.result = value


# 生成一个关于表达式的对象
class Expression:
    def __init__(self, expression, prefix, tree):
        self.prefix = prefix
        self.tree = tree
        self.expression = expression
        self.expression_add_space = ' '.join(expression)


# 辗转相除法求两整数最大公因数
def calculate_gcd(a, b):
    if a % b == 0:
        return b
    else:
        return calculate_gcd(b, a % b)


# 对分数约分
def reduce_fraction(fraction):
    s = fraction.split('/')
    common = calculate_gcd(int(s[0]), int(s[1]))
    return str(int(s[0]) // common) + '/' + str(int(s[1]) // common)


# 将分子大于分母的分数化为真分数
def true_fraction(numerator, denominator):
    numerator = int(numerator)
    denominator = int(denominator)
    remainder = numerator % denominator
    if remainder == 0:
        return str(numerator // denominator)
    elif numerator > denominator:
        return str(numerator // denominator) + '’' + reduce_fraction(str(remainder) + '/' + str(denominator))
    elif numerator < denominator:
        return reduce_fraction(str(remainder) + '/' + str(denominator))


# 中缀表达式转化为前缀表达式
def infix_prefix(str_list):
    str_list = str_list[:]
    s1 = []
    s2 = []
    order_dic = {'+': 0, '-': 0, '*': 1, '/': 1}

    def judge_priority(op):
        if len(s1) == 0 or s1[-1] == ')':  # S1为空或栈顶运算符为“)”，则直接入栈
            s1.append(op)
        elif order_dic[op] - order_dic[s1[-1]] >= 0:  # 若优先级比栈顶运算符的较高或相等，将运算符压入S1；
            s1.append(op)
        else:  # 否则将S1栈顶的运算符弹出并压入到S2中
            s2.append(s1.pop())
            judge_priority(op)

    while len(str_list):
        s = str_list.pop()
        if s in ['+', '-', '*', '/']:
            judge_priority(s)
        elif s == ')':  # 若为“)”，直接压入S1
            s1.append(s)
        elif s == '(':  # 若为“(”，依次弹出S1栈顶的运算符并压入S2
            while True:  # 直到遇到右括号，将这一对括号丢弃
                s = s1.pop()
                if s == ')':
                    break
                else:
                    s2.append(s)
        else:  # 遇到操作数压入S2
            s2.append(s)
    s2.reverse()
    prefix = s1 + s2
    return prefix


# 化为分数
def normalize_num(num):
    if num.find('’') > -1:
        split = num.split('’')
        integer = split[0]
        fraction = split[1]
        integration = fraction.split('/')
        numerator = integration[0]
        denominator = integration[1]
        return str(int(integer) * int(denominator) + int(numerator)) + '/' + denominator
    elif num.find('/') > -1:
        return num
    else:
        return num + '/' + '1'


# 判断两数运算结果符号以及是否可以运算
def operate(a, operator, b):
    if (not num_test(a)) or (not num_test(b)):
        return False
    a = normalize_num(a)
    b = normalize_num(b)
    result = 0

    # 通分
    def handle(num1, num2):
        num1 = num1.split('/')
        num2 = num2.split('/')
        d = int(num1[1]) * int(num2[1])
        n1 = int(num1[0]) * int(num2[1])
        n2 = int(num2[0]) * int(num1[1])
        return [[n1, n2], d]

    handle_num = handle(a, b)
    a_numerator = handle_num[0][0]
    b_numerator = handle_num[0][1]
    denominator = handle_num[1]
    if operator == '+':
        result = [a_numerator + b_numerator, denominator]
    elif operator == '-':
        result = [a_numerator - b_numerator, denominator]
    elif operator == '*':
        result = [a_numerator * b_numerator, denominator * denominator]
    elif operator == '/':
        result = [a_numerator, b_numerator]
    if result[0] < 0 or result[1] == 0:
        return False
    result = true_fraction(result[0], result[1])
    if not num_test(result):
        return False
    else:
        return result


# 测试数字是否符合题目要求
def num_test(num):
    if not num:
        return False
    num = str(num)
    if num.find('’') > -1:
        if int(num.split('’')[0]) < value_max and num_test(num.split('’')[1]):
            return True
        else:
            return False
    elif num.find('/') == -1:
        if int(num) > value_max:
            return False
        else:
            return True
    else:
        split_num = reduce_fraction(num).split('/')
        if int(split_num[0]) >= int(split_num[1]):
            return num_test(true_fraction(split_num[0], split_num[1]))
        else:
            return int(split_num[1]) <= value_max


# 将树化为前缀表达式
def tree_prefix(tree):
    prefix = []

    def traverse(t):
        if t is None:
            return
        prefix.append(t.value)
        traverse(t.lchild)
        traverse(t.rchild)

    traverse(tree)
    return prefix


# 将前缀表达式转化为二叉树
def prefix_tree(expression):
    expression = expression[:]
    expression.reverse()

    def traverse():
        if len(expression) > 0:
            value = expression.pop()
            node = TreeNode(value)
            if value in ['+', '-', '*', '/']:
                node.lchild = traverse()
                node.rchild = traverse()
            return node

    return traverse()


# 对树的节点进行计算并进行排序
def sort_tree(tree):
    if tree is None:
        return
    # 已经有结果直接退出
    if tree.result is not None:
        return
    sort_tree(tree.lchild)
    sort_tree(tree.rchild)
    if tree.value in ['+', '-', '*', '/']:
        tree.result = operate(tree.lchild.result,
                              tree.value, tree.rchild.result)
        # 加号和乘号重排序
        if tree.value in ['+', '*']:
            if tree.rchild.result is not False and tree.lchild.result is not False:
                if not operate(tree.rchild.result, '-', tree.lchild.result):
                    temp = tree.lchild
                    tree.lchild = tree.rchild
                    tree.rchild = temp


# 生成分数
def fraction_maker():
    dt = randint(2, value_max)
    nt = randint(1, dt - 1)
    return reduce_fraction(str(nt) + '/' + str(dt))


# 生成真分数
def num_maker():
    random_num = randint(1, 10)
    if random_num <= 6:
        result = randint(1, value_max)
    elif 7 <= random_num <= 9:
        result = fraction_maker()
    else:
        result = str(randint(1, value_max - 1)) + '’' + str(fraction_maker())
    return str(result)


# 生成运算符
def operator_maker():
    # random_num用于判定生成数的类型的概率
    random_num = randint(1, 10)
    if random_num <= 3:
        return '+'
    elif random_num <= 6:
        return '-'
    elif random_num <= 8:
        return '*'
    elif random_num <= 10:
        return '/'


# 确定操作数数量
def operand_num():
    expression = [num_maker()]
    num = randint(1, 3)
    while num:
        expression.append(operator_maker())
        expression.append(num_maker())
        num -= 1
    return expression


# 生成一个前缀表达式
def prefix_expression():
    exp = operand_num()
    prefix = infix_prefix(exp)
    tree = prefix_tree(prefix)
    sort_tree(tree)
    prefix = tree_prefix(tree)
    return Expression(exp, prefix, tree)


def main():
    collect = []
    result = []
    i = 0
    exercises = ''
    answer = ''
    while i < 8:
        collect.append([])
        i += 1
    collect_num = 0
    while collect_num < exercises_num:
        e = prefix_expression()
        no_repeat = len(list(filter(lambda n: n.expression_add_space == e.expression_add_space, collect[len(e.expression)]))) == 0
        if e.tree.result is not False and no_repeat:
            collect[len(e.expression)].append(e)
            collect_num += 1
    for c in collect:
        result.extend(c)
    for i in range(len(result)):
        exercises += (str(i + 1) + '. ' + result[i].expression_add_space + '\n')
        answer += (str(i + 1) + '. ' +
                   result[i].expression_add_space + ' = ' + result[i].tree.result + '\n')
    f_exercises = open('Exercises.txt', 'w', encoding="utf-8")
    f_exercises.write(exercises)
    f_exercises.close()
    f_answer = open('Answer.txt', 'w', encoding="utf-8")
    f_answer.write(answer)
    f_answer.close()


main()
