a = [1, 2, 3, 4, 5]
for i in a:
	print i
	if i % 2 == 0:
		a.remove(i)
print a