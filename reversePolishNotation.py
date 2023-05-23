#!/usr/bin/env python3
import tensorflow as tf
from log import log

OPERATORS = ('+', '-', '*', '(', ')')

PRIORITY = dict([
    ('+', 1),
    ('-', 1),
    ('*', 2)
])

P0=0
P1=0
P2=0


def pop_left_bracket(postfix, operators):
    while operators:
        operator = operators.pop()
        if operator == '(':
            break
        else:
            postfix.append(operator)

def compare_and_pop(i, postfix, operators):
    if len(operators) == 0:
        operators.append(i)
        return
    while operators:
        operator = operators.pop()
        if operator == '(':
            operators += ['(', i]
            return
        elif PRIORITY[i] > PRIORITY[operator]:
            operators += [operator, i]
            return
        else:
            postfix.append(operator)
    operators.append(i)


def pop_rest(postfix, operators):
    while operators:
        postfix.append(operators.pop())

def is_number(text):
    if text=='0' or text=='1' or text=='2':
        return True
    else:
        return False

def infix_to_arr(infix):
    infix = infix.replace(" ", "")
    infix = infix.replace('P0', '0')
    infix = infix.replace('P1', '1')
    infix = infix.replace('P2', '2')
    retArr = []
    for i in infix:
        retArr.append(i)
    return retArr


def infix_to_postfix(infix):
    infix = infix_to_arr(infix)
    print(222222222,infix)
    log(f"222222222,infix is {infix}")
    postfix = []
    operators = []
    for i in infix:
        if is_number(i):
            postfix.append(i)
        elif i in OPERATORS:
            if i == '(':
                operators.append(i)
            elif i == ')':
                pop_left_bracket(postfix, operators)
            else:
                compare_and_pop(i, postfix, operators)

    pop_rest(postfix, operators)

    return postfix

def get_party_data(a):
    if a=='0':
        return P0
    elif a=='1':
        return P1
    elif a == '2':
        return P2
    else:
        return a

def calc_two_parties(a,b,operand):
    matrix_a=get_party_data(a)
    matrix_b=get_party_data(b)
    if operand == '+':
        return tf.add(matrix_a, matrix_b)
    elif operand == '-':
        return tf.subtract(matrix_a, matrix_b)
    else:
        return tf.matmul(matrix_a, matrix_b)

def calc_postfix(postfix):
    operands = []
    for i in postfix:
        if is_number(i):
            operands.append(i)
        else:
            right = operands.pop()
            left = operands.pop()
            operands.append(calc_two_parties(left,right,i))

    print(333333333,operands)
    log(f"333333333,operands is {operands}")
    return operands[0]

def MatrixCombinationComputation(expression,matrix_a,matrix_b,matrix_c):
    global P0
    P0 = matrix_a
    global P1
    P1 = matrix_b
    global P2
    P2 = matrix_c
    postfix = infix_to_postfix(expression)

    if postfix is not None:
        print('Reverse polish notation is：%s' % ' '.join(postfix))
        postfixStr=' '.join(postfix)
        log(f"Reverse polish notation is {postfixStr}")
    else:
        print('Wrong expression！')
        log("Wrong expression！")
        exit()
    result = calc_postfix(postfix)
    print('Calc_postfix result：%s' % result)
    log(f"Calc_postfix result：{result}")
    return result

