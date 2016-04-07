from collections import namedtuple
_Person = namedtuple('Person','name age gender')

print type(_Person)
print _Person

Bob = _Person(name='Bob', age=30, gender='male')

