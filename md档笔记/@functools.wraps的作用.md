# @functools.wraps的作用

标签（空格分隔）： python

---

When you use a decorator, you're replacing one function with another. In other words, if you have a decorator
```
def logged(func):
    def with_logging(*args, **kwargs):
        print func.__name__ + " was called"
        return func(*args, **kwargs)
    return with_logging
```
then when you say:
```
@logged
def f(x):
   """does some math"""
   return x + x * x
```
it's exactly the same as saying:
```
def f(x):
    """does some math"""
    return x + x * x
f = logged(f)
```
and your function f is replaced with the function with_logging. Unfortunately, this means that if you then say

`print f.__name__`
it will print with_logging because that's the name of your new function. In fact, if you look at the docstring for f, it will be blank because with_logging has no docstring, and so the docstring you wrote won't be there anymore. Also, if you look at the pydoc result for that function, it won't be listed as taking one argument x; instead it'll be listed as taking *args and **kwargs because that's what with_logging takes.

If using a decorator always meant losing this information about a function, it would be a serious problem. That's why we have functools.wraps. This takes a function used in a decorator and adds the functionality of copying over the function name, docstring, arguments list, etc. And since wraps is itself a decorator, the following code does the correct thing:
```
from functools import wraps
def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print func.__name__ + " was called"
        return func(*args, **kwargs)
    return with_logging

@logged
def f(x):
   """does some math"""
   return x + x * x

print f.__name__  # prints 'f'
print f.__doc__   # prints 'does some math'
```



