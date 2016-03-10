# mysql修改表属性

tags : MYSQL
---
添加列属性：

 1. 默认加在表的最后面：
`ALTER TABLE user1 ADD age TINYINT UNSIGNED NOT NULL DEFAULT 10;`
 2. 加在指定列后面：
`ALTER TABLE user1 ADD paaword VARCHAR(20) NOT NULL AFTER username;`
 3. 加在最前面：
  `ALTER TABLE user1 ADD truename VARCHAR(20) NOT NULL FIRST;`

---
删除列属性：

 1. 删除一列
  `ALTER TABLE user1 DROP truename;`
 2. 删除多列：
 `ALTER TABLE user1 DROP password, DROP age;`

---
添加/删除主键约束：

 1. 添加主键约束：
 `ALTER TABLE user2 ADD CONSTRAINT PK_user2_id PRIMARY KEY (id);`
 2. 删除主键约束：
 `ALTER TABLE user2 DROP PRIMARY KEY;`


---
添加/删除唯一约束：

 1. 添加唯一约束:
`ALTER TABLE user2 ADD UNIQUE (username);`
 2. 删除唯一约束
 `ALTER TABLE user2 DROP INDEX username;`

---
添加/删除外键约束：

 1. 添加外键约束：
 `ALTER TABLE user2 ADD FOREIGN KEY (pid) REFERENCES provinces (id);`
注释：
外键表和主键表需要有相同的存储引擎，以及类似对应的数据类型。
 2. 删除外加约束：
 `ALTER TABLE user2 DROP FOREIGN KEY user2_ibfk_1;`
注释：
此处的"user2_ibfk_1"是通过"SHOW CREATE TABLE user2"得到的。

此时外键约束上有索引还未有删除，删除方式是：
 `ALTER TABLE user2 DROP INDEX pid;`

---
添加/删除默认约束：

 1. 添加默认约束：
 `ALTER TABLE user2 ALTER age SET DEFAULT 15;`
 2. 删除默认约束：
`ALTER TABLE user2 ALTER age DROP DEFAULT;`

---
修改列定义：

 1. 修改某列在表中的位置：
 例如：
 `ALTER TABLE user2 MODIFY id SMALLINT UNSIGNED NOT NULL FIRST;`
 2. 修改列名称：
 ` ALTER TABLE user2 CHANGE pid p_id SMALLINT UNSIGNED NOT NULL;`
 3. 修改列定义：
  上面两句话都可以修改列定义，直接将"SMALLINT"修改成想要的类型即可。

---
修改表名称：

 1. 方法1：
 `ALTER TABLE user2 RENAME user3;`
 2. 方法2：
 `RENAME TABLE user3 TO user2;`
 

 

