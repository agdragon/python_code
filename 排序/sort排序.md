#python中的sort方法使用详解

###概述:
Python中的sort()方法用于数组排序，是List的成员函数

##**内容**

* 目录：
    * [基本形式](#user-content-基本形式)
    * [自定义比较函数](#user-content-自定义比较函数)
    * [可选参数](#user-content-可选参数)

<br>


* ####基本形式：
	列表有自己的sort方法，其对列表进行原址排序，既然是原址排序，那显然元组不可能拥有这种方法，因为元组是不可修改的。

		x = [4, 6, 2, 1, 7, 9]
		x.sort()
		print x # [1, 2, 4, 6, 7, 9]

	如果需要一个排序好的副本，同时保持原有列表不变，怎么实现呢?

		x =[4, 6, 2, 1, 7, 9]
		y = x[ : ]
		y.sort()
		print y #[1, 2, 4, 6, 7, 9]
		print x #[4, 6, 2, 1, 7, 9]

	注意：y = x[:] 通过分片操作将列表x的元素全部拷贝给y，如果简单的把x赋值给y：y = x，y和x还是指向同一个列表，并没有产生新的副本。

	另一种获取已排序的列表副本的方法是使用sorted函数：

		x =[4, 6, 2, 1, 7, 9]
		y = sorted(x)
		print y #[1, 2, 4, 6, 7, 9]
		print x #[4, 6, 2, 1, 7, 9]

	sorted返回一个有序的副本，并且类型总是列表，如下：

		print sorted('Python') #['P', 'h', 'n', 'o', 't', 'y']

* ####自定义比较函数：
    可以定义自己的比较函数，然后通过参数传递给sort方法：

    	def comp(x, y):
			if x < y:
				return 1
			elif x > y:
				return -1
			else:
				return 0
			 
			nums = [3, 2, 8 ,0 , 1]
			nums.sort(comp)
			print nums # 降序排序[8, 3, 2, 1, 0]
			nums.sort(cmp) # 调用内建函数cmp ，升序排序
			print nums # 降序排序[0, 1, 2, 3, 8]

* ####可选参数：
	sort方法还有两个可选参数：key和reverse

		1. key在使用时必须提供一个排序过程总调用的函数：

			x = ['mmm', 'mm', 'mm', 'm' ]
			x.sort(key = len)
			print x # ['m', 'mm', 'mm', 'mmm']

		2. reverse实现降序排序，需要提供一个布尔值：

			y = [3, 2, 8 ,0 , 1]
			y.sort(reverse = True)
			print y #[8, 3, 2, 1, 0]
	