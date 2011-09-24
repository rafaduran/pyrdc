#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
:py:mod:`~decorators.class` --- Class decorators
================================================
Long description

.. module:: decorators.class
    :synopsis: This module contains class decorators

.. moduleauthor::"Rafael Durán Castañeda <rafadurancastaneda@gmail.com>"
"""

class Singleton(object):
    """
    :py:class:`Singleton` class decorator implements 
    `singleton pattern <http://en.wikipedia.org/wiki/Singleton_pattern>`_. It 
    uses static methods, so there is not need to be instantiated itself. When a
    new instance is requested via :py:func:`get_instance` static method, 
    Singleton creates a key based on given class name and arguments and tries to
    return an instance matching this key, if a `KeyError` exception occur it
    will create a new instance and it will add the new instance to a Python
    dictionary.
    
    Usage::
        
        @Singleton.get_instance
        class A(object):
            def __init__(self,*args,**kwargs):
                print("args:{0}".format([arg for arg in args]))
                print("kwargs:{0}".format([item for item in kwargs.items()]))
                
    Now you can try it::
    
        >>> spam = A([1,2])
        args:[[1, 2]]
        kwargs:[]
        >>> eggs = A(3,y=2,x=4)
        args:[3]
        kwargs:[('y', 2), ('x', 4)]
        >>> yam = A(3,x=4,y=2)
        >>> print(id(spam),id(eggs),id(yam))
        139944850546256 139944850546576 139944850546576
    """
    __instances = {}
    
    @staticmethod
    def get_instance(cls):
        def inner(*args, **kwargs):
            key = Singleton.to_key(cls,*args,**kwargs)
            try:
                return Singleton.__instances[key]
            except KeyError:
                instance = cls(*args, **kwargs)
                Singleton.__instances[key] = instance
                return instance
        return inner


    @staticmethod
    def to_key(cls, *args, **kwargs):
        return "{0}{1}{2}".format(cls, args, sorted(kwargs.items()))

