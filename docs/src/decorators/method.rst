.. automodule :: pyrdc.decorators.method
    :members: optional_arguments_decorator, memoized


.. py:function:: pyrdc.decorators.method.error_wrapper(func, args, kwargs, errors=(Exception,), msg="Unknown error", error_func=print)

    :py:func:`error_wrapper` wrappes any given number of exceptions, if no errors
    agrument is provided then wrappes :py:exc:`Exception` and applies error_func when 
    an errors occur(default builtin print function, imported from future).
    
    Args:
        func, args, kwargs: needed by :py:func:`optional_arguments_decorator`
        errors: errors to be wrapped. Exception tuple, default :py:class:`Exception`
        msg: A message can be included here
        error_func: Callable accepting two arguments (Exception raised, message
            from previous attribute) that will be called if an error occurs.
        
    :Authors: Rafael Durán Castañeda <rafadurancastaneda@gmail.com>
    
    Usage::
    
        @error_wrapper(errors=(TypeError, ValueError, ZeroDivisionError))
        def test(a, b):
            return a / b
        
    And then you'll get:
        
    >>> test(9, 0)
    integer division or modulo by zero
    >>> test(5, "string")
    unsupported operand type(s) for /: 'int' and 'str'
    
    This works nice with partial::
    
        import functools
        
        os_io_error_wrapper = functools.partial(error_wrapper, errors=(IOError, OSError))
        
        @os_io_error_wrapper
        def test():
            file = open("Doesn't exist", "rb")
            
    so:
    
        >>> test()
        [Errno 2] No such file or directory: "Doesn't exist"
   

