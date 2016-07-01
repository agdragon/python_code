from weakref import WeakKeyDictionary

class NonNegative(object):
    """A descriptor that forbids negative values"""
    def __init__(self, default):
        self.default = default
        self.data = WeakKeyDictionary()

    def __get__(self, instance, owner):
        # we get here when someone calls x.d, and d is a NonNegative instance
        # instance = x
        # owner = type(x)
        return self.data.get(instance, self.default)

    def __set__(self, instance, value):
        # we get here when someone calls x.d = val, and d is a NonNegative instance
        # instance = x
        # value = val
        if value < 0:
            raise ValueError("Negative value not allowed: %s" % value)
        self.data[instance] = value

class Movie(object):

    #always put descriptors at the class-level
    rating = NonNegative(0)
    runtime = NonNegative(0)
    budget = NonNegative(0)
    gross = NonNegative(0)

    def __init__(self, title, rating, runtime, budget, gross):
        self.title = title
        self.rating = rating
        self.runtime = runtime
        self.budget = budget
        self.gross = gross

    def profit(self):
        return self.gross - self.budget

m = Movie('Casablanca', 97, 102, 964000, 1300000)
print m.budget  # calls Movie.budget.__get__(m, Movie)
m.rating = 100  # calls Movie.budget.__set__(m, 100)
try:
    m.rating = -1   # calls Movie.budget.__set__(m, -100)
except ValueError:
    print "Woops, negative value"

'''
访问描述符

当解释器遇到print m.buget时，它就会把budget当作一个带有__get__ 方法的描述符，调用Movie.budget.__get__方法并将方法的返回值打印出来，而不是直接传递m.budget来打印。这和你访问一个property相似，Python自动调用一个方法，同时返回结果。

__get__接收2个参数：一个是点号左边的实例对象（在这里，就是m.budget中的m），另一个是这个实例的类型（Movie）。在一些Python文档中，Movie被称作描述符的所有者（owner）。如果我们需要访问Movie.budget，Python将会调用Movie.budget.__get__(None, Movie)。可以看到，第一个参数要么是所有者的实例，要么是None。这些输入参数可能看起来很怪，但是这里它们告诉了你描述符属于哪个对象的一部分。当我们看到NonNegative类的实现时这一切就合情合理了。

对描述符赋值

当解释器看到m.rating = 100时，Python识别出rating是一个带有__set__方法的描述符，于是就调用Movie.rating.__set__(m, 100)。和__get__一样，__set__的第一个参数是点号左边的类实例（m.rating = 100中的m）。第二个参数是所赋的值（100）。

删除描述符

为了说明的完整，这里提一下删除。如果你调用del m.budget，Python就会调用Movie.budget.__delete__(m)。
'''