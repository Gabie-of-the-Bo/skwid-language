from inspect import isfunction
from skwid_functools import left_compose, left_bind, add_kwargs, flatten, combinator
from typing import List, Set

import numpy as np

"""
===========================================
| くコ:彡 (The Skwid Programming Language) |
===========================================

This is the official implementation of the くコ:彡 programming language (Skwid from now on).

"""

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
        '¡': lambda i: i + 1,
        '&': lambda i, j: np.array([i]*j),
        'ι': lambda i, j: np.arange(i, j),
        '∑': lambda i: np.sum(i),
        'Π': lambda i: np.product(i),
        'μ': lambda i: np.mean(i),
        '!': lambda i, j: i[j],

        # Logic operators
        '∃': lambda i: np.any(i),
        '∀': lambda i: np.all(i),
        '¬': lambda i: not i,

        # Higher order
        '$': lambda i, j: np.array(list(map(j, i))),

        # IO
        '>': lambda i: print(i),
    }

    def __init__(self, functions=[]):
        self.functions = functions
    
    def get(self, index):
        return self.functions[index]

class Skwid_token:
    NUM, VAR, FUN, REF, COM = range(5)

    def __init__(self, rep, token_type, flatten=False):
        self.rep = rep
        self.token_type = token_type
        self.flatten = flatten

    def is_number(self):
        return self.token_type == Skwid_token.NUM

    def is_variable(self):
        return self.token_type == Skwid_token.VAR

    def is_function(self):
        return self.token_type == Skwid_token.FUN

    def is_ref(self):
        return self.token_type == Skwid_token.REF

    def is_combinator(self):
        return self.token_type == Skwid_token.COM

    def __repr__(self):
        if not self.is_ref():
            return str(self.rep)

        return ('@' if flatten else '#') + str(self.rep)    

def tokenize(code: str) -> List[Skwid_token]:
    is_az = lambda c: ord('A') <= ord(c.upper()) <= ord('Z')

    if code == '`':
        return [Skwid_token('', Skwid_token.COM)]

    if all(i.isdigit() for i in code):
        return [Skwid_token(int(code), Skwid_token.NUM)]

    if all(is_az(i) for i in code):
        return [Skwid_token(code, Skwid_token.VAR)]

    signature = lambda c: (c.isdigit(), is_az(c), c == '(', c in '#@', c == '`')

    for i in range(len(code) - 1):
        if code[i] in '#@':
            tokens = tokenize(code[1:])

            if tokens[0].is_function() or tokens[0].is_ref():
                tokens = [Skwid_token('', Skwid_token.VAR)] + tokens
            
            tokens[0] = Skwid_token(tokens[0].rep, Skwid_token.REF, code[i] == '@')

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

def parse(code: str, variables=None) -> Skwid_context:
    def parse_rec(tokens: List[Skwid_token], contexts, variables: Set[str], args=False):

        t = tokens[0]
        
        if len(tokens) == 1:
            if t.is_number():
                return t.rep

            if t.is_variable():
                return eval('lambda *,{}:{}'.format(','.join('{}=None'.format(i) for i in variables), t))

            if t.is_function():
                return add_kwargs(Skwid_context.__func_table__[t.rep], variables)

            if t.is_ref():
                if t.flatten:
                    ref = contexts[t.rep]
                    return add_kwargs(flatten(ref), variables) if isfunction(ref) else ref

                return contexts[t.rep]

        if is_enclosed(tokens):
            return parse_rec(tokens[1:-1], contexts, variables, args)

        if t.is_combinator():
            return add_kwargs(combinator(parse_rec(tokens[1:], contexts, variables, args)), variables)

        if args:
            start = 0
            func_args = []

            while tokens:
                index = is_tuple(tokens)

                if index:
                    func_args.append(parse_rec(tokens[:index], contexts, variables))
                    tokens = tokens[(index + 1):]
                
                else:
                    func_args.append(parse_rec(tokens, contexts, variables))
                    tokens = None

            return func_args

        if t.rep != '(' and (t.is_function() or t.is_ref()):
            f = parse_rec([t], contexts, variables, args)
            args = parse_rec(tokens[1:], contexts, variables, True)

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

        return 'NOT_IMPL'

    functions = [tokenize(j.replace(' ', '')) for i in code.split('\n') if i for j in i.split('|') if j]
    variables = [list(sorted({t.rep for t in tokens if t.is_variable()})) for tokens in functions]

    for i, tokens in enumerate(functions):
        for ref in (t.rep for t in tokens if t.is_ref() and not t.flatten):
            variables[i] += variables[ref]

        variables[i] = list(sorted(set(variables[i])))

    contexts = []

    for t, v in zip(functions, variables):
        contexts.append(parse_rec(t, contexts, v))

    return Skwid_context(contexts)

def compile(code: str):
    return parse(code).functions[-1]