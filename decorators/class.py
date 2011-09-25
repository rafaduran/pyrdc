#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
:py:mod:`~pyrdc.decorators.class` --- Class decorators
======================================================
This module contains class decorators.

.. module:: pyrdc.decorators.class
    :synopsis: This module contains class decorators

.. moduleauthor::"Rafael Durán Castañeda <rafadurancastaneda@gmail.com>"
"""

class Singleton(object):
    """
    :py:class:`Singleton` class decorator implements 
    `singleton pattern <http://en.wikipedia.org/wiki/Singleton_pattern>`_. It 
    uses static methods, so there is not need to be instantiated itself. When a
    new instance is requested via :py:meth:`Singleton.get_instance` static method, 
    Singleton creates a key based on given class name and arguments and tries to
    return an instance matching this key, if a :py:exc:`KeyError` exception occur it
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
    
def dict_from_class(cls, filtered=()):
    """
    Returns a dictionary containing all attributes for a given class, 
    filtering unwanted attributes. This method is needed by 
    :py:func:`property_from_class`.
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
    
    .. warning:::py:func:`exception_wrapper` uses 
        :py:func:`dict_from_class`, so it must be used together or imported
        
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
        
    """
    return property(doc=cls.__doc__, **dict_from_class(cls))

