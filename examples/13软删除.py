# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  13软删除.py
@Time    :  2022/7/16 0:14
@Author  :  张大鹏
@Version :  v0.1.0
@Contact :  lxgzhw@163.com
@License :  (C)Copyright 2022-2023
@Desc    :  演示软删除功能的实现
"""
from zdppy_orm import *
from zdppy_orm.mysql_ext import JSONField
from zdppy_orm.model import MysqlDatabase, SoftDeleteModel

db = MysqlDatabase("zdppy_orm", host="127.0.0.1", port=3306, user="root", password="root")


class BaseModel(SoftDeleteModel):
    class Meta:
        database = db


class Category(BaseModel):
    """
    分类模型
    """
    name = CharField(max_length=20, verbose_name="名称")
    parent_category = ForeignKeyField("self", verbose_name="父类别", null=True)  # 一级类别可以没有父类别
    level = IntegerField(default=1, verbose_name="级别")
    is_tab = BooleanField(default=False, verbose_name="是否显示在首页tab")


class Brands(BaseModel):
    """
    品牌模型
    """
    name = CharField(max_length=50, verbose_name="名称", index=True, unique=True)
    logo = CharField(max_length=200, null=True, verbose_name="图标", default="")


class Goods(BaseModel):
    """
    商品， 分布式的事务最好的解决方案 就是不要让分布式事务出现
    """
    category = ForeignKeyField(Category, verbose_name="商品类目", on_delete='CASCADE')
    brand = ForeignKeyField(Brands, verbose_name="品牌", on_delete='CASCADE')
    on_sale = BooleanField(default=True, verbose_name="是否上架")
    goods_sn = CharField(max_length=50, default="", verbose_name="商品唯一货号")
    name = CharField(max_length=100, verbose_name="商品名")
    click_num = IntegerField(default=0, verbose_name="点击数")
    sold_num = IntegerField(default=0, verbose_name="商品销售量")
    fav_num = IntegerField(default=0, verbose_name="收藏数")
    market_price = FloatField(default=0, verbose_name="市场价格")
    shop_price = FloatField(default=0, verbose_name="本店价格")
    goods_brief = CharField(max_length=200, verbose_name="商品简短描述")
    ship_free = BooleanField(default=True, verbose_name="是否承担运费")
    images = JSONField(verbose_name="商品轮播图")
    desc_images = JSONField(verbose_name="详情页图片")
    goods_front_image = CharField(max_length=200, verbose_name="封面图")
    is_new = BooleanField(default=False, verbose_name="是否新品")
    is_hot = BooleanField(default=False, verbose_name="是否热销")


class GoodsCategoryBrand(BaseModel):
    """
    品牌分类
    """
    id = AutoField(primary_key=True, verbose_name="id")
    category = ForeignKeyField(Category, verbose_name="类别")
    brand = ForeignKeyField(Brands, verbose_name="品牌")

    class Meta:
        indexes = (
            # 联合主键
            (("category", "brand"), True),
        )


class Banner(BaseModel):
    """
    轮播的商品
    """
    image = CharField(max_length=200, default="", verbose_name="图片url")
    url = CharField(max_length=200, default="", verbose_name="访问url")
    index = IntegerField(default=0, verbose_name="轮播顺序")


if __name__ == "__main__":
    models = [Category, Goods, Brands, GoodsCategoryBrand, Banner]
    db.drop_tables(models)
    db.create_tables(models)

    # 添加数据
    c1 = Category(name="图书", level=1)
    c2 = Category(name="数码产品", level=1)
    c1.save()
    c2.save()

    # 查询
    for c in Category.select():
        print(c.name, c.id, c.is_deleted)
    print("=======")

    # 强制删除
    c1.delete_instance(permanently=True)

    # 查询
    for c in Category.select():
        print(c.name, c.id, c.is_deleted)
    print("=======")

    # 软删除
    Category.delete().where(Category.id == 2).execute()

    # 查询
    for c in Category.select():
        print(c.name, c.id, c.is_deleted)
