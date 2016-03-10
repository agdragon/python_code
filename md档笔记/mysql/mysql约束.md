#mysql约束

tags : MYSQL

---
作用：
    保证数据的完整性和一致性

---
分类：
    表级约束和列级约束
    列级约束：约束只针对某一个字段来使用，就是列级约束。
    表级约束：约束针对两个或者两个以上的字段来使用，就是表级约束。
    
---
功能分类:
    NOT NULL(非空约束)
    PRIMARY KEY(主键约束)
    UNIQUE KEY(唯一约束)
    DEFAULT(默认约束)
    FOREIGN KEY(外键约束)
    
    
---
外键约束的要求：

 1. 父表和子表必须使用相同的存储引擎，而且禁止使用临时表。
 2. 数据表的存储引擎只能为InnoDB。
 3. 外键列和参照列必须具有相似的数据类型。其中数字的长度或是否有符号位必须相同；而字符的长度可以不相同。
 4. 外键列和参照列必须创建索引。如果外键列不存在索引的话，MySql将自动创建索引。
 注释：
    父表：有主键的那个
    子表：有外键的那个表


---
外键约束的参照操作：
 1. CASCADE:从父表中删除或更新且自动删除或更新子表中匹配的行。
 2. 外键约束下的表，父表修改后，子表是否进行修改。
SET NULL：从父表删除或更新行，并设置子表中的外键列为NULL；
RESTRICT:拒绝对父表的删除或更新操作；
NO ACTION:标准SQL的关键字，在MySQL中与RESTRICT相同。
FOREIGN KEY (key_name) REFERENCEES table_name (key_name) ON DELETE CASCADE；
ON DELETE \ ON UPDATE
插入记录时，需先在父表中插入记录，而后才能在子表中插入记录

总结：
![总结](D:\code\note\mysql\约束和表属性.png)