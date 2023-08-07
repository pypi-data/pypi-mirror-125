math_eval
============

*Safe evaluation of strings as math expressions*


Features
--------

* Written entirely in Python.
* Read strings representing math expressions or functions of any number of variables, and return a scalar or function as appropriate.
* Supports all logical and arithmetic operators, as well as arbitrary functions of one or two variables.
* Easy to add new functions of one or two variables.
* safe_compute adds an extra layer of safety by creating functions that refuse non-numeric inputs.
* Equation class that can be extended independently of compute() and safe_compute().

How to use
----------

* Install Python 3.6 or newer.
* Install

    ```sh
    # or PyPI
    pip install math_eval
    ```

* Use in situations where you need safe evaluation of strings as math expressions

    ```py
    >>> from math_eval import compute, safe_compute
    >>> fun = safe_compute("x*y")
    >>> fun('a', 3)
    Traceback (most recent call last):
    ...
    ValueError: Functions produced by compute() with safe = True do not accept non-numeric arguments.
    >>> fun(3.4, 3)
    10.2
    >>> fun2 = compute("str(z) + x*y")
    >>> fun2('a', 3, 3.5)
    '3.5aaa'
    >>> print(fun2.__doc__)
    str(z) + x*y
    Args are positional-only in the order ['x', 'y', 'z'].
    >>> compute("(3*4.5**2 >= 17) | 1/-5 == 3")
    True
    ```
	
**WARNING**
`safe_compute()` is *not* safe if arbitrary ufunctions are added, and `compute()` is probably unsafe in countless ways I haven't thought of as it is. 

For instance, if the `chr` and `eval` ufunctions were introduced, even `safe_compute()` could be used to evaluate artibrary Python expressions by translating integers into strings, and evaluating those strings with the normal Python interpreter.

I (Mark J. Olson) am *not* knowledgeable about computer security, so think carefully about possible workarounds for safe_compute's safety features before deploying it in a safety-sensitive setting.


Contributing
------------

Be sure to read the [contribution guidelines]

(https://github.com/molsonkiko/math_eval/blob/main/CONTRIBUTING.md). 


More information
------------
TODO: add something to show test coverage of code (Coverage URL does not exist)

[![Coverage](https://codecov.io/github/URL-OF-PROJECT?branch=master)](https://codecov.io/OTHER-URL-OF-PROJECT)