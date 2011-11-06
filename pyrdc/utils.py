#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
"""
:py:mod:`~pyrdc.utils` --- Utils mix
====================================
This module contains a mix of Python methods

.. module:: pyrdc.utils
    :synopsis: Some miscellaneous helper functions

.. moduleauthor::"Rafael Durán Castañeda <rafadurancastaneda@gmail.com>"
"""
import hashlib


def unique_list(seq):
    """
    This method converts an iterable into a list with no repeated values
    (a unique list). I took this method from Cal Leeming "Django site with
    40mil+ rows of data" speech.

    :Authors: Dave Kirby
    """
    seen = set()
    return [item for item in seq if item not in seen and not seen.add(item)]


def merged_list(sequence):  # Dave Kirby
    """
    This method merges an iterable into a plain list. I took this method from
    Cal Leeming "Django site with 40mil+ rows of data" speech and I improved
    it myself.

    """
    merged = []
    for seq in sequence:
        try:
            for item in seq:
                merged.append(item)
        except TypeError:
            merged.append(item)
    return merged


def md5(value):
    """
    This method returns md5 hashed for the given value. I took this method
    from Cal Leeming "Django site with 40mil+ rows of data" speech.
    """
    hashed = hashlib.md5()
    hashed.update(str(value))
    return hashed.hexdigest()


def to_key(name, *args, **kwargs):
    """
    Returns an string formed by the provided name, args and kwargs. This
    string can be used as a key for caching purposes.
    """
    return "{0}{1}{2}".format(name, args, sorted(kwargs.items()))
