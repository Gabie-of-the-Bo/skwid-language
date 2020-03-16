import skwid
import skwid_functools

def basic_tests():
    code = '12\n/1,2|#2'
    code = skwid.parse(code)
    res = [12, 0.5, 'NOT_IMPL']

    for i, j in zip(code.functions, res):
        if i != j:
            print('Basic tests: incorrect {} -> {}'.format(i, j))
            return

    print('Basic tests: Success!')

def function_tests_1():
    code = '∑X'
    code = skwid.parse(code)
    code = [code.get(0)(X=i) for i in range(1, 6)]
    res = [1, 2, 3, 4, 5]

    for i, j in zip(code, res):
        if i != j:
            print('Function tests 1: incorrect {} -> {}'.format(i, j))
            return

    print('Function tests 1: Success!')

def function_tests_2():
    code = '∑ιX,100'
    code = skwid.parse(code)
    code = [code.get(0)(X=i) for i in range(100)]
    res = [sum(range(i, 100)) for i in range(100)]

    for i, j in zip(code, res):
        if i != j:
            print('Function tests 2: incorrect {} -> {}'.format(i, j))
            return

    print('Function tests 2: Success!')

def function_tests_3():
    code = '∑ιX,Y'
    code = skwid.parse(code)
    
    for i in range(100):
        for j in range(100):
            r1 = code.get(0)(X=i, Y=j)
            r2 = code.get(0)(Y=j, X=i)

            if r1 != r2 or r1 != sum(range(i, j)):
                print('Function tests 3: incorrect {}, {} -> {}, {}'.format(i, j, r1, r2))
                return


    print('Function tests 3: Success!')

def naive_primality_test(values):
    template = '∀%X,(ι2,X)'
    code = skwid.parse(template).get(0)

    for i in values:        
        res = code(X=i)

        if res != all(i % j for j in range(2, i)):
            print('Naive primality test: incorrect {} -> {}'.format(i, res))
            return

    print('Naive primality test: Success!')

basic_tests()
function_tests_1()
function_tests_2()
function_tests_3()
naive_primality_test(range(2, 100))