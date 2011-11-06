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


class Borg(object):
    """
    :py:class:`Borg` class decorator implements Borg design pattern. Sharing
    is done by :py:meth:`~pyrdc.patterns.Borg.share` static method, decorating
    class __init__ method first time a new object is requested. __init__
    will initialize objects only first once for each parameter set, sharing
    __dict__ attribute after that.

    Usage::

        @Borg.share
        class Shared(object):
            def __init__(self, x):
                self.x = x

        ham = Shared(3)     # Object is initialized
        eggs = Shared(3)    # eggs and ham are shared objects
        ham.x = 2           # This change affects both 
        spam = Shared(1)    # Spam is not shared, since initialization 
                            # attributes are different
        print(id(ham), id(eggs), id(spam))
        print(id(ham.__dict__), id(eggs.__dict__), id(spam.__dict__))
        print(ham.x, eggs.x, spam.x)
    """
    __shared = {}

    @staticmethod
    def share(cls):
        def outer_inner(*args, **kwargs):
            def decorate(func):
                def inside_inner(self, *args, **kwargs):
                    key = utils.to_key(cls, *args, **kwargs)
                    try:
                        # Coping attributes if already initiliazed
                        self.__dict__ = Borg.__shared[key]
                    except KeyError:
                        # Initialization
                        self.__dict__ = Borg.__shared[key] = {}
                        func(self, *args, **kwargs)
                return inside_inner
            # Decorating __init__ method only if it isn't decorated
            try:
                cls.__decorated
            except AttributeError:
                cls.__decorated = True
                cls.__init__ = decorate(cls.__init__)
            return cls(*args, **kwargs)
        return outer_inner
