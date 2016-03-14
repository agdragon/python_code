#mysql索引的一个技巧

###概述:
mysql索引的一个技巧


##**内容**

* 目录：
    * [文章](#user-content-文章)

<br>

 
* ####文章：
    针对一下`sql`语句:

    	`select * from table where col1 > number order by col2 desc`。

	其实按照常规的方法可以这样设计：`key(col1, col2)`

	但是这种办法在`mysql`里不算是理想的，`where`条件里限定索引前部分是一个范围的情况下后面的`order by`还是会有`filesort`。如果`where`条件里限定索引前部分是一个常量，那么`order by`就会有效利用索引。例如：

		`select * from table where col1 = number order by col2 desc，explain`

	的结果就不错。


	为了让它能够利用上索引并且消除`filesort`，可以这样设计
	索引：`key(col2,col1)`

		`select * from table where col2 > min_value and col1 > number order by col2 desc`

	这里`where`条件里同时执行了索引的两个列，并且为了保证逻辑一致，对`col2`列的限定条件等效于无限定。

	这样`mysql`就能很好的利用索引了。这个技巧在`mysql high performance2`里也有提过.