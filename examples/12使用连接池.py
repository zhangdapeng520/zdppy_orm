# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@File    :  12使用连接池.py
@Time    :  2022/7/16 0:14
@Author  :  张大鹏
@Version :  v0.1.0
@Contact :  lxgzhw@163.com
@License :  (C)Copyright 2022-2023
@Desc    :  描述
"""
from zdppy_orm import *
from zdppy_orm.pool import PooledMySQLDatabase
from zdppy_orm.shortcuts import ReconnectMixin


# 使用连接池， 使用ReconnectMixin来防止出现连接断开查询失败
class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass


DB = ReconnectMysqlDatabase("zdppy_orm", host="127.0.0.1", port=3306, user="root", password="root")


class BaseModel(Model):
    class Meta:
        database = DB


class User(BaseModel):
    # 用户模型
    GENDER_CHOICES = (
        ("female", "女"),
        ("male", "男")
    )

    ROLE_CHOICES = (
        (1, "普通用户"),
        (2, "管理员")
    )

    mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号码")
    password = CharField(max_length=100, verbose_name="密码")  # 1. 密文 2. 密文不可反解
    nick_name = CharField(max_length=20, null=True, verbose_name="昵称")
    head_url = CharField(max_length=200, null=True, verbose_name="头像")
    birthday = DateField(null=True, verbose_name="生日")
    address = CharField(max_length=200, null=True, verbose_name="地址")
    desc = TextField(null=True, verbose_name="个人简介")
    gender = CharField(max_length=6, choices=GENDER_CHOICES, null=True, verbose_name="性别")
    role = IntegerField(default=1, choices=ROLE_CHOICES, verbose_name="用户角色")


if __name__ == "__main__":
    DB.create_tables([User])
