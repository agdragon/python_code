# mysql随机查询若干条数据的方法

标签（空格分隔）： MYSQL

---

这篇文章主要介绍了mysql中获取随机内容的方法：
在mysql中查询5条不重复的数据，使用以下代码：
```
SELECT * FROM `table` ORDER BY RAND() LIMIT 5
```
这条sql语句就可以，但是真正测试一下才发现这样效率非常低。一个15万余条的库，查询5条数据，居然要8秒以上
搜索`Google`，网上基本上都是查询`max(id) * rand()`来随机获取数据。代码如下:
```
SELECT * 
FROM `table` AS t1 JOIN (SELECT ROUND(RAND() * (SELECT MAX(id) FROM `table`)) AS id) AS t2 
WHERE t1.id >= t2.id 
ORDER BY t1.id ASC LIMIT 5;
```
但是这样会产生连续的`5`条记录。解决办法只能是每次查询一条，查询`5`次。即便如此也值得，因为`15`万条的表，查询只需要`0.01`秒不到。
上面的语句采用的是`JOIN`，`mysql`的论坛上有人使用如下代码:
```
SELECT * 
FROM `table` 
WHERE id >= (SELECT FLOOR( MAX(id) * RAND()) FROM `table` ) 
ORDER BY id LIMIT 1;
```
我测试了一下，需要`0.5`秒，速度也不错，但是跟上面的语句还是有很大差距。总觉有什么地方不正常。
于是我把语句改写了一下。如下代码:
```
SELECT * FROM `table` 
WHERE id >= (SELECT floor(RAND() * (SELECT MAX(id) FROM `table`)))  
ORDER BY id LIMIT 1;
```
这下，效率又提高了，查询时间只有`0.01`秒
最后，再把语句完善一下，加上`MIN(id)`的判断。我在最开始测试的时候，就是因为没有加`上MIN(id)`的判断，结果有一半的时间总是查询到表中的前面几行。
完整查询语句是：
复制代码 代码如下:
```
SELECT * FROM `table` 
WHERE id >= (SELECT floor( RAND() * ((SELECT MAX(id) FROM `table`)-(SELECT MIN(id) FROM `table`)) + (SELECT MIN(id) FROM `table`)))  
ORDER BY id LIMIT 1;
SELECT * 
FROM `table` AS t1 JOIN (SELECT ROUND(RAND() * ((SELECT MAX(id) FROM `table`)-(SELECT MIN(id) FROM `table`))+(SELECT MIN(id) FROM `table`)) AS id) AS t2 
WHERE t1.id >= t2.id 
ORDER BY t1.id LIMIT 1;
```
最后对这两个语句进行分别查询`10`次，
前者花费时间 `0.147433` 秒
后者花费时间 `0.015130` 秒
看来采用`JOIN`的语法比直接在`WHERE`中使用函数效率还要高很多。






