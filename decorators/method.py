#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
:py:mod:`~pyrdc.decorators.method` --- Method decorators
========================================================
This module contains method decorators.

.. module:: pyrdc.decorators.method 
    :synopsis: Method decorators
    
.. moduleauthor::"Rafael Durán Castañeda <rafadurancastaneda@gmail.com>"
"""
import functools

def optional_arguments_decorator(real_decorator):
    """
    :py:func:`optional_arguments_decorator` is a decorator factory, so a 
    function is converted in a new decorator that can be used with or without 
    arguments. This receipt has been taken from  chapter 2 of 
    Martyn Alchin's "Pro Django" book.
    
    .. note::
        Decorators using this receipt must used extra arguments as keywords 
        arguments
        
    Usage example::
       
        @optional_arguments_decorator
        def decorate(func, args, kwargs, prefix='Decorated'):
            return '{0}: {1}'.format(prefix, func(*args, **kwargs))
            
        @decorate
        def test(a, b):
            return a + b
            
    And then:: 

        >>> print(test(13,4))
        Decorated: 17
        >>> test = decorate(test, prefix='Decorated again')
        >>> print(test(13,4))
        Decorated again: Decorated: 17
    """
    def decorator(func=None, **kwargs):
        # This is the decorator that will be
        # exposed to the rest of your program
        def decorated(func):
            # This returns the final, decorated
            # function, regardless of how it was called
            def wrapper(*a, **kw):
                return real_decorator(func, a, kw, **kwargs)
            return wrapper
        if func is None:
            # The decorator was called with arguments
            def decorator(func):
                return decorated(func)
            return decorator
        # The decorator was called without arguments
        return decorated(func)
    return decorator


class memoized(object):
    """
    :py:class:`memoized` decorator caches a function's return value each time 
    it is called. If called later with the same arguments, the cached value is 
    returned, and not re-evaluated. This decorator recipe has been taking from 
    `Python decorators libray <http://wiki.python.org/moin/PythonDecoratorLibrary>`_
    
    Usage::
    
        @memoized
        def fibonacci(n):
           "Return the nth fibonacci number."
           if n in (0, 1):
              return n
           return fibonacci(n-1) + fibonacci(n-2)

    Then::
    
        >>> print fibonacci(12)
        144
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
        def __repr__(self):
            """Return the function's docstring."""
            return self.func.__doc__
        def __get__(self, obj, objtype):
            """Support instance methods."""
            return functools.partial(self.__call__, obj)
