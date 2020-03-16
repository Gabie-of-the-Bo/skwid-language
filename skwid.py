from inspect import isfunction
from skwid_functools import left_compose, left_bind, add_kwargs
from typing import List, Set

import numpy as np

"""
===========================================
| くコ:彡 (The Skwid Programming Language) |
===========================================

This is the official implementation of the くコ:彡 programming language (Skwid from now on).

"""

class Skwid_expression:
    pass

class Skwid_context:
    __func_table__ = {
        # Basic operators
        '+': lambda i, j: i + j,
        '-': lambda i, j: i - j,
        '*': lambda i, j: i * j,
        '/': lambda i, j: i / j,
        '%': lambda i, j: i % j,
        '^': lambda i, j: i ** j,
        '=': lambda i, j: i == j,
        
        # Basic functions
        '&': lambda i, j: np.array([i]*j),
        'ι': lambda i, j: np.arange(i, j),
        '∑': lambda i: np.sum(i),
        'Π': lambda i: np.product(i),
        'μ': lambda i: np.mean(i),

        # Logic operators
        '∃': lambda i: any(i),
        '∀': lambda i: all(i),
        '¬': lambda i: not i,

        # IO
        '>': lambda i: print(i),
    }

    def __init__(self, functions=[]):
        self.functions = functions
    
    def get(self, index):
        return self.functions[index]

class Skwid_token:
    NUM, VAR, FUN, REF = range(4)

    def __init__(self, rep, token_type):
        self.rep = rep
        self.token_type = token_type

    def is_number(self):
        return self.token_type == Skwid_token.NUM

    def is_variable(self):
        return self.token_type == Skwid_token.VAR

    def is_function(self):
        return self.token_type == Skwid_token.FUN

    def is_ref(self):
        return self.token_type == Skwid_token.REF

    def __repr__(self):
        if not self.is_ref():
            return str(self.rep)

        return '#' + str(self.rep)    

def tokenize(code: str) -> List[Skwid_token]:
    is_az = lambda c: ord('A') <= ord(c.upper()) <= ord('Z')

    if all(i.isdigit() for i in code):
        return [Skwid_token(int(code), Skwid_token.NUM)]

    if all(is_az(i) for i in code):
        return [Skwid_token(code, Skwid_token.VAR)]

    signature = lambda c: (c.isdigit(), is_az(c), c == '(')

    for i in range(len(code) - 1):
        if code[i] == '#':
            tokens = tokenize(code[1:])

            if tokens[0].is_function() or tokens[0].is_ref():
                tokens = [Skwid_token('', Skwid_token.VAR)] + tokens
            
            tokens[0] = Skwid_token(tokens[0].rep, Skwid_token.REF)

            return tokens
        
        if signature(code[i]) != signature(code[i + 1]): # Signature change
            return tokenize(code[:(i + 1)]) + tokenize(code[(i + 1):])
    
    return [Skwid_token(i, Skwid_token.FUN) for i in code]

def is_tuple(tokens):
    count = 0

    for i, t in enumerate(tokens):
        if t.rep == '(':
            count += 1
        
        elif t.rep == ')':
            count -= 1
        
        if t.rep == ',' and count == 0:
            return i

    return False

def is_enclosed(tokens):
    count = 0

    for i, t in enumerate(tokens):
        if t.rep == '(':
            count += 1
        
        if count == 0:
            return False
        
        elif t.rep == ')':
            count -= 1

    return count == 0

def parse(code: str, variables=set()) -> Skwid_context:
    if '\n' in code:
        return Skwid_context(list(parse(j).functions[0] for i in code.split('\n') if i for j in i.split('|') if j))

    def parse_rec(tokens: List[Skwid_token], variables: Set[str], args=False):
        t = tokens[0]
        
        if len(tokens) == 1:
            if t.is_number():
                return t.rep

            if t.is_variable():
                return eval('lambda *,{}:{}'.format(','.join('{}=None'.format(i) for i in variables), t))

            if t.is_function():
                return add_kwargs(Skwid_context.__func_table__[t.rep], variables)

        if is_enclosed(tokens):
            return parse_rec(tokens[1:-1], variables, args)

        if t.rep != '(' and t.is_function():
            f = add_kwargs(Skwid_context.__func_table__[t.rep], variables)
            args = parse_rec(tokens[1:], variables, True)

            if not isinstance(args, list):
                args = [args]

            while args:
                last, args = args[0], args[1:]

                if isfunction(last):
                    f = left_compose(f, last, variables)

                else:
                    f = left_bind(f, last, variables)

            return f if f.__code__.co_argcount or f.__code__.co_kwonlyargcount else f()

        if not args and (t.is_number() or t.is_variable()):
            raise RuntimeError('Invalid composition with {} as operand'.format(t))

        if args:
            start = 0
            func_args = []

            while tokens:
                index = is_tuple(tokens)

                if index:
                    func_args.append(parse_rec(tokens[:index], variables))
                    tokens = tokens[(index + 1):]
                
                else:
                    func_args.append(parse_rec(tokens, variables))
                    tokens = None

            return func_args

        return 'NOT_IMPL'

    tokens = tokenize(code.replace(' ', ''))

    if not variables:
        variables = list(sorted({t.rep for t in tokens if t.is_variable()}))

    return Skwid_context([parse_rec(tokens, variables)])