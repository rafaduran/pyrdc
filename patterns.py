#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
:py:mod:`~pyrdc.patterns` --- Patterns
======================================
This module contains Python implementations for some common patterns (actually
just singleton). 

.. module:: pyrdc.patterns
    :synopsis: This module contains patterns implementations

.. moduleauthor::"Rafael Durán Castañeda <rafadurancastaneda@gmail.com>"
"""
import utils


class Singleton(object):
    """
    :py:class:`Singleton` class decorator implements 
    `singleton pattern <http://en.wikipedia.org/wiki/Singleton_pattern>`_. It 
    use static method decorator :py:meth:`get_instance` and a class variable, 
    so there is not need to be instantiated itself. When a new instance is 
    requested via Singleton it creates a key value based on the given class 
    name and arguments, trying to return an instance matching this key, 
    if a :py:exc:`KeyError` exception occur it will create a new instance 
    and it will add the new instance to a Python sdictionary.
    
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
            key = utils.to_key(cls,*args,**kwargs)
            try:
                return Singleton.__instances[key]
            except KeyError:
                instance = cls(*args, **kwargs)
                Singleton.__instances[key] = instance
                return instance
        return inner