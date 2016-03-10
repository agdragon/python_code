# mysql查询笔记

tags： MYSQL

---
#查询表达式
每一个表达式表示想要的一列，必须有最少一个。
多个列之间以英文逗号分隔
星号(*)表示所有列，tb1_name.*可以表示命名表的所有列
查询表达式可以使用[AS] alias_name 为其赋予别名
别名可用于GROUP BY，ORDER BY或者HAVING子句

---
# order by
- 对查询结果进行排序
```
order by{col_name}
select * from users order by id desc; //对一个字段排序
select * from users order by age,id desc; //两个字段同时排序
```

- desc是降序
- 对查询结果进行排序：
```
[ORDER BY [col_name | expr | position ]` [ASC|DESC],...]
select * from user order by id desc;
```
- 可以同时按多条字段进行排序，规则是先按前面的字段排，在基础上再按后面字段排。
如：
```
SELECT * FROM users ORDER BY age,id DESC;
先按照age排序，如果age有重复的，重复的字段里按id排序
```
---

#limit用法
```
select * from users limit 2 ；从第一条开始返回，返回前两个；
select * from users limit 3,2 ；忽略前三条，从第四条开始，取前两条；
```

---
#将查询出的数据插入到指定表的指定字段中
```
insert table_name(column_name) select column_name from table_name1;
```

---
#总结
```
INSERT [INTO] tbl_name [(col_name,...)] {VALUES | VALUE} ({expr|DEFAULT},...),(...),...
INSERT [INTO] tbl_name SET col_name={expr|DEFAULT},...
INSERT [INTO] tbl_name [(col_name,...)] SELECT...

UPDATE://更新数据
单表更新/UPDATE [LOW_PRIORITY][IGNORE] table_reference SET col_name1={expr1|DEFAULT},[col_name2={expr2|DEFAULT}]...[WHERE where_condition]
多表更新/...

DELETE : //删除数据
单表删除/DELETE FROM tbl_name [WHERE where_condition}
多表删除/...

SELECT: //查询
SELECT select_expr [,select_expr ...]
[
FROM
WHERE
GROUP BY {col_name | position}[ASC|DESC],...
LIMIT {[offset,] row_count|row_count OFFSET offset}
```



