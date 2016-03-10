# mysql插入记录
tags : MYSQL
---
1. **最基础的插入 INSERT VALUES**
 - 可以给自动编号字段赋值：NULL或者DEFAULT
 - 有默认值的字段可以赋值：DEFAULT获取默认值
 - value里面可以使用函数或者表达式
 - INSERT 表名（字段1，字段2……）VALUES(值1，值2……)，（值3，值4……）
2. **高级方法 INSERT SET**
 - 与基础查询的区别是，该方法可以使用子查询。上面的方法可以一次性插入多条数据，这种方式只能插入一条数据。
`INSERT users SET username='Ben',password='123';`

3. **高级方法 INSERT SELECT**
- 此方法可以将查询结果插入到指定的数据表。

4. 总结
```
insert into 表名 values （null 或default ，值2，     值3，...），（null或default，值3，值4，....）;
insert 表名 （字段1，字段2，....） values （ 值1，值2，...），（值3，值4，...）;
`insert 表名 set 字段1=值1， 字段2=值2，... ;
```

