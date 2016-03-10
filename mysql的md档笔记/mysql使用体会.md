# mysql使用体会

tags: MYSQL
---
- **批量导入sql文件到mysql**
vim all.sql
在里面写入：
`source 1.sql
source 2.sql
......
source 53.sql
source 54.sql`
然后只要
`mysql> source all.sql`

我看到还有人尝试用 source *.sql 来执行，这样是不行的（哥也尝试了一下）。
值得注意一点的是，all.sql加载进来的sql文件最好写绝对路径，否则会找不到文件，除非你是在.sql的同级目录底下启用的mysql

如果两个在线的网站互转数据，解决就更简单了：
mysqldump -uuser -ppwd database | mysql -hip -ppwd database
*user为数据库用户名；pwd为数据库密码；ip为数据库ip；database为数据库名字；另外后面为目标库*

---

 - **MySQL ON vs USING?**
ON is the more general of the two. One can join tables ON a column, a set of columns and even a condition. For example:

`SELECT * FROM world.City JOIN world.Country ON (City.CountryCode = Country.Code) WHERE ...`
USING is useful when both tables share a column of the exact same name on which they join. In this case, one may say:

`SELECT ... FROM film JOIN film_actor USING (film_id) WHERE ...`
An additional nice treat is that one does not need to fully qualify the joining columns:

`SELECT film.title, film_id # film_id is not prefixed
FROM film
JOIN film_actor USING (film_id)
WHERE ...`
To illustrate, to do the above with ON, we would have to write:

`SELECT film.title, film.film_id # film.film_id is required here
FROM film
JOIN film_actor ON (film.film_id = film_actor.film_id)
WHERE ...`
Notice the film.film_id qualification in the SELECT clause. It would be invalid to just say film_id since that would make for an ambiguity:

ERROR 1052 (23000): Column 'film_id' in field list is ambiguous
As for select *, the joining column appears in the result set twice with ON while it appears only once with USING:

`mysql> create table t(i int);insert t select 1;create table t2 select*from t;`
Query OK, 0 rows affected (0.11 sec)

Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

Query OK, 1 row affected (0.19 sec)
Records: 1  Duplicates: 0  Warnings: 0

`mysql> select*from t join t2 on t.i=t2.i;`
| i    | i    |
|:----:|:----:|
|    1 |    1 |
`1 row in set (0.00 sec)`

`mysql> select*from t join t2 using(i);`
| i    |
|:----:|
|    1 |
`1 row in set (0.00 sec)`





