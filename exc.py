#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
:py:mod:`~pyrdc.exc` --- Exception handlers utils
=================================================
This module contains some handy exception handlers.

.. module:: pyrdc.exc
    :synopsis: Exception handlers utils
    
.. moduleauthor::"Rafael Durán Castañeda <rafadurancastaneda@gmail.com>"
"""
from __future__ import print_function


def wrapper(func, args, kwargs, errors=Exception, 
                  msg="Unknown error", error_func=print):
    try:
        return func(*args, **kwargs)
    except errors as e:
        return error_func(e, msg)