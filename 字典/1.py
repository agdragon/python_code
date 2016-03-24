#!/user/bin/python
# -*- coding: utf-8 -*-

a = {"a":1,"b":2}
b = {"a":2}

tmp_dict = {
	"a":a,
	"b":b
}

for key,value in a.items():
	value = 100
print a


for key,value in tmp_dict.items():
	value["a"] = 10
print tmp_dict

'''
#- 结果:

	{'a': 1, 'b': 2}
	{'a': {'a': 10, 'b': 2}, 'b': {'a': 10}}

'''