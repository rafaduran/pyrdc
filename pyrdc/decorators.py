#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
:py:mod:`~pyrdc.decorators` --- Decorators
==========================================
This module contains some handy decorators.

.. module:: pyrdc.decorators
    :synopsis: Decorators
    
.. moduleauthor::"Rafael Durán Castañeda <rafadurancastaneda@gmail.com>"
"""
from __future__ import print_function
import functools

import pyrdc.utils as utils
from pyrdc.exc import wrapper

def optional_arguments_decorator(real_decorator):
    """
    :py:func:`optional_arguments_decorator` is a decorator factory, so a 
    function is converted in a new decorator that can be used with or without 
    arguments. This receipt has been taken from  chapter 2 of 
    Martyn Alchin's "Pro Django" book.
    
    Args:
        real_decorator. Function to be converted into a new decorator
    
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
    and imporved, so it accepts keywords arguments too.
    
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
    def __call__(self, *args, **kwargs):
        try:
            return self.cache[utils.to_key(self.func, *args, **kwargs)]
        except KeyError:
            value = self.cache[utils.to_key(self.func, *args, **kwargs)] =\
                self.func(*args, **kwargs)
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args, **kwargs)
        def __repr__(self):
            """Return the function's docstring."""
            return self.func.__doc__
        def __get__(self, obj, objtype):
            """Support instance methods."""
            return functools.partial(self.__call__, obj)


def dict_from_class(cls, filtered=()):
    """
    Returns a dictionary containing all attributes for a given class, 
    filtering unwanted attributes. This method is needed by 
    :py:func:`property_from_class`.
    
    :authors: Jonathan Fine, 
        Rafael Durán Castañeda <rafadurancastaneda@gmail.com>
    """
    return dict(
        (key, value)
        for (key, value) in cls.__dict__.items()
        if key not in filtered  and not(key.startswith('__') and \
                                       key.endswith('__')))


def property_from_class(cls):
    """
    Class decorator used to build a property attribute from a class. 
    
    This decorator receipt was taken from 
    `Jonathan Fine speech at Europython 2011
    <http://ep2011.europython.eu/conference/talks/objects-and-classes-in-python-and-javascript>`_
    
    :authors: Jonathan Fine
        
    Usage::
        
        class A(object):
            @property_from_class 
            class value(object):
                '''Value must be an integer'''
                def fget(self):
                    return self.__value
                def fset(self, value):
                    # Ensure that value to be stored is an int.
                    assert isinstance(value, int), repr(value)
                self.__value = value

    Now you can do::
        
        >>> a = A()
        >>> a.value = 4
        >>> print(a.value)
        4
        >>> print(A.value.__doc__)
        Value must be an integer
        >>> a.value = 'hola'
        Traceback (most recent call last):
          File "/home/rdc/workspace/pyrdc/test.py", line 82, in <module>
            a.value = 'hola'
          File "/home/rdc/workspace/pyrdc/test.py", line 75, in fset
            assert isinstance(value, int), repr(value)
        AssertionError: 'hola'
        print("factorial: {0}".format(factorial(5)))
    """
    return property(doc=cls.__doc__, **dict_from_class(cls))


error_wrapper = optional_arguments_decorator(wrapper)