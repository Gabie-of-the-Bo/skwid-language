import skwid
import skwid_functools

import numpy as np

def basic_tests():
    code = '12\n/1,2|#0'
    code = skwid.parse(code)
    res = [12, 0.5, 12]

    for i, j in zip(code.functions, res):
        if i != j:
            print('Basic tests: incorrect {} -> {}'.format(i, j))
            return

    print('Basic tests: Success!')

def function_tests_1():
    code = '∑X'
    code = skwid.compile(code)
    code = [code(X=i) for i in range(1, 6)]
    res = [1, 2, 3, 4, 5]

    for i, j in zip(code, res):
        if i != j:
            print('Function tests 1: incorrect {} -> {}'.format(i, j))
            return

    print('Function tests 1: Success!')

def function_tests_2():
    code = '∑ιX,100'
    code = skwid.compile(code)
    code = [code(X=i) for i in range(100)]
    res = [sum(range(i, 100)) for i in range(100)]

    for i, j in zip(code, res):
        if i != j:
            print('Function tests 2: incorrect {} -> {}'.format(i, j))
            return

    print('Function tests 2: Success!')

def function_tests_3():
    code = '∑ιX,Y'
    code = skwid.compile(code)
    
    for i in range(50):
        for j in range(50):
            r1 = code(X=i, Y=j)
            r2 = code(Y=j, X=i)

            if r1 != r2 or r1 != sum(range(i, j)):
                print('Function tests 3: incorrect {}, {} -> {}, {}'.format(i, j, r1, r2))
                return


    print('Function tests 3: Success!')

def naive_primality_test(values):
    template = '∀%X,ι2,X'
    code = skwid.compile(template)

    for i in values:        
        res = code(X=i)

        if res != all(i % j for j in range(2, i)):
            print('Naive primality test: incorrect {} -> {}'.format(i, res))
            return

    print('Naive primality test: Success!')

def mse_test(values1, values2):
    template = 'μ^-X,Y,2'
    code = skwid.compile(template)

    for i, j in zip(values1, values2):
        r1 = code(X=i, Y=j)
        r2 = code(Y=j, X=i)

        if r1 != r2 or r1 != np.mean((i - j)**2):
            print('Mean Square Error test: incorrect {} -> {}'.format(i, res))
            return

    print('Mean Square Error test: Success!')

def composed_naive_primality_test(values):
    template1 = 'ι2,X|%X,#0|∀#1'
    template2 = 'ι2,X|%X,#0|∀@1'
    code1 = skwid.compile(template1)
    code2 = skwid.compile(template2)

    for i in values:        
        r1 = code1(X=i)
        r2 = code2(i)

        if r1 != r2 or r1 != all(i % j for j in range(2, i)):
            print('Composed naive primality test: incorrect {} -> {}, {}'.format(i, r1, r2))
            return

    print('Composed naive primality test: Success!')

def naive_prime_list_test(limit):
    template1 = 'ι2,X|∀%X,#0|!#0,$#0,`@1|@2'
    template2 = '∀%X,ι2,X|?ι2,X,`@0|@1'
    template3 = """
    ∀%X,ι2,X    [Naive primality test]
    ?ι2,X,`@0   [Filter list starting from two]
    @1          [Flatten result]
    """
    code1 = skwid.compile(template1)
    code2 = skwid.compile(template2)
    code3 = skwid.compile(template3)
    
    r1 = code1(limit)
    r2 = code2(limit)
    r3 = code3(limit)
    sol = np.array([i for i in range(2, limit) if all(i % j for j in range(2, i))])

    if any(r1 != r2) or any(r1 != r3) or any(r1 != sol):
        print('Naive prime list test: incorrect {} -> {}, {}, {}'.format(sol, r1, r2, r3))

    print('Naive prime list test: Success!')

basic_tests()
function_tests_1()
function_tests_2()
function_tests_3()
naive_primality_test(range(2, 100))
mse_test([np.random.rand(100) for i in range(30)], [np.random.rand(100) for i in range(30)])
composed_naive_primality_test(range(2, 100))
naive_prime_list_test(100)