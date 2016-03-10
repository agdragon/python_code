# insert ... select用法以及多表更新

tags： MYSQL

---

    ```
    INSERT tdb_goods_cates(cate_name) SELECT goods_cate FROM tdb_goods GROUP BY goods_cate;
    ```




