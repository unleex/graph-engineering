import typing

def chain_functions(*functions: list[typing.Callable]) -> typing.Callable:

    def chained(*args, **kwargs):
        for function in functions:
            if not isinstance(args, tuple):
                args = [args]
            args = function(*args, **kwargs)
        return args
    
    return chained