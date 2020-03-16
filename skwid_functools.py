def left_compose(f, p, kwargs): # Construct lambda
    rem_args = p.__code__.co_argcount
    rest_args = f.__code__.co_argcount - 1
    lbody = 'lambda {}{}{}{}{}: f(p({}),{}{}{})'
    largs = ','.join('a' + str(i) for i in range(rem_args))
    rargs = ','.join('b' + str(i) for i in range(rest_args))
    kwargs_l = ','.join('{}=None'.format(i) for i in kwargs)
    kwargs_r = ','.join('{}={}'.format(i, i) for i in kwargs)
    comma = ',' if rem_args and rest_args else ''
    comma2 = ',' if (rem_args or rest_args) and kwargs else ''
    astrk = '*,' if kwargs else ''

    return eval(lbody.format(largs, comma, rargs, comma2 + astrk, kwargs_l, largs + comma + kwargs_r, rargs, comma2, kwargs_r), {'f':f, 'p':p})

def left_bind(f, arg, kwargs):
    rem_args = f.__code__.co_argcount - 1
    lbody = 'lambda {}{}{}: f(arg,{}{}{})'
    largs = ','.join('a' + str(i) for i in range(rem_args))
    rargs = ','.join('b' + str(i) for i in range(1))
    kwargs_l = ','.join('{}=None'.format(i) for i in kwargs)
    kwargs_r = ','.join('{}={}'.format(i, i) for i in kwargs)
    comma = ',' if rem_args else ''
    comma2 = ',' if comma and kwargs else ''
    comma3 = ',' if kwargs else ''
    astrk = '*,' if kwargs else ''

    return eval(lbody.format(largs, comma2 + astrk, kwargs_l, largs, comma2, kwargs_r), {'f':f, 'arg':arg})

def add_kwargs(f, kwargs):
    rem_args = f.__code__.co_argcount
    lbody = 'lambda {}{}{}: f({})'
    largs = ','.join('a' + str(i) for i in range(rem_args))
    kwargs_l = ','.join('{}=None'.format(i) for i in kwargs)
    kwargs_r = ','.join('{}={}'.format(i, i) for i in kwargs)
    comma = ',' if rem_args and kwargs else ''
    astrk = '*,' if kwargs else ''

    return eval(lbody.format(largs, comma + astrk, kwargs_l, largs, comma, kwargs_r), {'f':f})
