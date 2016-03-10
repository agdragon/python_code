# MySQL分组排序

标签（空格分隔）： MYSQL

---

在一个表中取出根据某个字段排序并根据另一个字段分组的若干条数据，你会怎么写SQL？

如有一张记录用户登录的表（用户每登录一次都会在表中记录），要查询最后3个登录的用户及时间。

假设表结构如下:
`mysql> desc table_test;`
|Field   |Type            |Null|Key|Default|Extra|
|--------|----------------|----|---|-------|-----|
|Id      |int(10) unsigned|NO  |PRI|NULL   |auto_increment|
|UserId  |int(10) unsigned|NO  |   |NULL   |              |
|UserName|varchar(255)    |NO  |   |NULL   |              |
|Time    |datetime        |NO  |   |NULL   |              |

查询表的数据:
`mysql> select * from table_test;`
| Id | UserId | UserName | Time                |
|----|--------|----------|---------------------|
|  1 |   1223 | test1    | 2011-12-05 21:46:32 |
|  2 |   1224 | test2    | 2011-12-13 21:46:56 |
|  3 |   1225 | test3    | 2011-12-14 21:47:24 |
|  4 |   1223 | test1    | 2011-12-16 21:47:37 |
|  5 |   1223 | test1    | 2011-12-16 21:47:50 |
|  6 |   1224 | test2    | 2011-12-17 21:48:02 |
|  7 |   1225 | test3    | 2011-12-19 21:48:16 |
|  8 |   1223 | test1    | 2011-12-21 21:50:58 |
|  9 |   1226 | test4    | 2011-12-23 21:51:27 |
| 10 |   1223 | test1    | 2011-12-24 21:52:05 |

很容易写出这样的SQL：
`mysql> select UserId, UserName, Time from table_test group by UserId order by Time desc limit 3;`
得到如下结果:
| UserId | UserName | Time                |
|--------|----------|---------------------|
|   1226 | test4    | 2011-12-23 21:51:27 |
|   1225 | test3    | 2011-12-14 21:47:24 |
|   1224 | test2    | 2011-12-13 21:46:56 |

很明显，这不是最近登录的3个用户，这样写是不对的。

分析一下，这是因为MySQL先执行了group by，按`UserId`进行了分组，分组的过程中按照默认排序（这里是主键升序）每个用户取出一条记录，相当于执行：
`mysql> select * from table_test group by UserId;`
| Id | UserId | UserName | Time                |
|----|--------|----------|---------------------|
|  1 |   1223 | test1    | 2011-12-05 21:46:32 |
|  2 |   1224 | test2    | 2011-12-13 21:46:56 |
|  3 |   1225 | test3    | 2011-12-14 21:47:24 |
|  9 |   1226 | test4    | 2011-12-23 21:51:27 |

然后再对取出来的数据用`Time`字段排序，最后取出前3条，相当于：
`mysql> select UserId, UserName, Time from(select * from table_test group by UserId) t order by Time desc limit 3;`
| UserId | UserName | Time                |
|--------|----------|---------------------|
|   1226 | test4    | 2011-12-23 21:51:27 |
|   1225 | test3    | 2011-12-14 21:47:24 |
|   1224 | test2    | 2011-12-13 21:46:56 |


正确地写法这里介绍两种，第一种采用子查询：
```mysql> select `UserId`, `UserName`, `Time`
    -> from (
    -> 	select `UserId`, `UserName`, `Time`
    ->  from `table_test`
    ->  order by `Time` desc
    -> ) t
    -> group by t.`UserId`
    -> order by t.`Time` desc
    -> limit 3;```
| UserId | UserName | Time                |
|--------|----------|---------------------|
|   1223 | test1    | 2011-12-24 21:52:05 |
|   1226 | test4    | 2011-12-23 21:51:27 |
|   1225 | test3    | 2011-12-19 21:48:16 |
效果达到了，性能如何呢：


```
mysql> explain select `UserId`, `UserName`, `Time`
    -> from (
    -> 	select `UserId`, `UserName`, `Time`
    ->  from `table_test`
    ->  order by `Time` desc
    -> ) t
    -> group by t.`UserId`
    -> order by t.`Time` desc
    -> limit 3;```

| id | select_type | table      | type | possible_keys | key  | key_len | ref  | rows | Extra                           |
|----|-------------|------------|------|---------------|------|---------|------|------|---------------------------------|
|  1 | PRIMARY     | <derived2> | ALL  | NULL          | NULL | NULL    | NULL |   10 | Using temporary; Using filesort |
|  2 | DERIVED     | table_test | ALL  | NULL          | NULL | NULL    | NULL |   10 | Using filesort                  |

执行计划很糟糕：全表扫描，Using filesort，Using temporary。即使`UserId`和`Time`字段加上索引也无济于事。

再看第二种方法：
`mysql> select UserId, UserName, max(Time) as MaxTime from table_test group by UserId order by MaxTime desc limit 3;`
| UserId | UserName | MaxTime             |
|--------|----------|---------------------|
|   1223 | test1    | 2011-12-24 21:52:05 |
|   1226 | test4    | 2011-12-23 21:51:27 |
|   1225 | test3    | 2011-12-19 21:48:16 |

执行计划如下：
`mysql> explain select UserId, UserName, max(Time) as MaxTime from table_test group by UserId order by MaxTime desc limit 3;`
| id | select_type | table      | type  | possible_keys | key          | key_len | ref  | rows | Extra                           |
|----|-------------|------------|-------|---------------|--------------|---------|------|------|---------------------------------|
|  1 | SIMPLE      | table_test | index | NULL          | index_userid | 4       | NULL |   10 | Using temporary; Using filesort |
type为index，`UserId`字段上的索引也发挥了作用:)




