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
    classes first time a new object of that class is requested. __init__ method
    is decorated when slots aren' used, just sharing __dict__ attribute. 
    However since this won't work on slots, slots are handled using properties.

    Usage::

        @Borg.share
        class Shared(object):
            def __init__(self, x):
                self.x = x


    Now you can::
 
        >>> ham = Shared(3)     # Object is initialized
        >>> eggs = Shared(3)    # eggs and ham are shared objects
        >>> ham.x = 2           # This change affects both
        >>> print(id(ham), id(eggs))
        (140294276774800, 140294276775056)
        >>> print(id(ham.__dict__), id(eggs.__dict__))
        (19432688, 19432688)
        >>> print(ham.x, eggs.x)
        (2, 2)
    
    This works on slots too::

        @Borg.share
        class Shared(object):
            __slots__ = ('x',)
            def __init__(self, x):
                self.x = x

    So::
    
        >>> ham = Shared(3)     # Object is initialized
        >>> eggs = Shared(3)    # eggs and ham are shared objects
        >>> print(ham.x, eggs.x)
        (3, 3)
        >>> ham.x = 2           # This change affects both
        >>> print(ham.x, eggs.x)
        (2, 2)
        >>> spam = Shared(1)    # Now all 3 objects are changed
        print(ham.x, eggs.x, spam.x)
        (1, 1, 1)
        
    .. warning::
    
        Note that each time a new object is requested attributes are shared,
        but __init__ is executed, so if this isn't the desired behavior you
        should modify __init__ method.
    """
    __shared = {}

    @staticmethod
    def share(cls):
        def outer_inner(*args, **kwargs):
            # decorate decorates __init__ method when no __slots__ are found
            def decorate(func):
                key = utils.to_key(cls)
                def inner(self, *args, **kwargs):
                    try:
                        # Sharing
                        self.__dict__ = Borg.__shared[key]
                    except KeyError:
                        # Start sharing
                        self.__dict__ = Borg.__shared[key] = {}
                    finally:
                        # Initialization
                        func(self, *args, **kwargs)
                return inner
            # class decorator starts here.
            try:
                # Check if already decorated
                cls.__decorated
            except AttributeError:
                # Decorating
                cls.__decorated = True
                if not '__slots__' in dir(cls):
                    # If no __slots__  decorating __init__
                    cls.__init__ = decorate(cls.__init__)
                else:
                    # When __slots__ are found setting properties for each
                    # slot
                    key = utils.to_key(cls)
                    Borg.__shared[key] = {}
                    for slot in cls.__slots__:
                        def setter(self, value):
                            Borg.__shared[key][slot] = value
                        def getter(self):
                            try:
                                return Borg.__shared[key][slot]
                            except KeyError:
                                return None
                        setattr(cls, slot, property(getter, setter))
            return cls(*args, **kwargs)
        return outer_inner
