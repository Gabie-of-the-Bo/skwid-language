def get_lhandside(pargs, fargs, kwargs):
    pargs = ['b{}'.format(i) for i in range(pargs)]
    fargs = ['a{}'.format(i) for i in range(fargs)]
    kwargs = ['{}=None'.format(i) for i in kwargs]
    
    if kwargs:
        kwargs = ['*'] + kwargs

    return ','.join(pargs + fargs + kwargs)

def get_lhandside_flatten(fargs, kwargs):
    fargs = ['a{}'.format(i) for i in range(fargs)]
    kwargs = ['{}0'.format(i) for i in kwargs]

    return ','.join(fargs + kwargs)

def get_rhandside(fargs, kwargs):
    fargs = ['a{}'.format(i) for i in range(fargs)]
    kwargs = ['{}={}'.format(i, i) for i in kwargs]

    return ','.join(fargs + kwargs)

def get_rhandside_flatten(fargs, kwargs):
    fargs = ['a{}'.format(i) for i in range(fargs)]
    kwargs = ['{}={}0'.format(i, i) for i in kwargs]

    return ','.join(fargs + kwargs)

def get_rhandside_compose(pargs, fargs, kwargs):
    pargs = ['b{}'.format(i) for i in range(pargs)]
    fargs = ['a{}'.format(i) for i in range(fargs)]
    kwargs = ['{}={}'.format(i, i) for i in kwargs]
    p = 'p({})'.format(','.join(pargs + kwargs))

    return ','.join([p] + fargs + kwargs)

def left_compose(f, p, kwargs): # Construct lambda
    lbody = 'lambda {}: f({})'

    pargs = p.__code__.co_argcount
    fargs = f.__code__.co_argcount - 1
    lhandside = get_lhandside(pargs, fargs, kwargs)
    rhandside = get_rhandside_compose(pargs, fargs, kwargs)

    return eval(lbody.format(lhandside, rhandside), {'f':f, 'p':p})

def left_bind(f, arg, kwargs):
    lbody = 'lambda {}: f(arg,{})'

    fargs = f.__code__.co_argcount - 1
    lhandside = get_lhandside(0, fargs, kwargs)
    rhandside = get_rhandside(fargs, kwargs)

    return eval(lbody.format(lhandside, rhandside), {'f':f, 'arg':arg})

def add_kwargs(f, kwargs):
    rem_args = f.__code__.co_argcount
    lbody = 'lambda {}{}{}: f({})'
    largs = ','.join('a' + str(i) for i in range(rem_args))
    kwargs_l = ','.join('{}=None'.format(i) for i in kwargs)
    kwargs_r = ','.join('{}={}'.format(i, i) for i in kwargs)
    comma = ',' if rem_args and kwargs else ''
    astrk = '*,' if kwargs else ''

    return eval(lbody.format(largs, comma + astrk, kwargs_l, largs, comma, kwargs_r), {'f':f})

def flatten(f):
    lbody = 'lambda {}: f({})'

    vs = list(sorted(f.__kwdefaults__.keys() if f.__kwdefaults__ else []))
    lhandside = get_lhandside_flatten(f.__code__.co_argcount, vs)
    rhandside = get_rhandside_flatten(f.__code__.co_argcount, vs)

    return eval(lbody.format(lhandside, rhandside), {'f':f})