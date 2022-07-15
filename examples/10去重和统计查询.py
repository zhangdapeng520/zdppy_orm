import datetime

from zdppy_orm import *
import logging

logger = logging.getLogger("zdppy_orm")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

db = MySQLDatabase('zdppy_orm', host='127.0.0.1', user='root', passwd='root')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()

    class Meta:
        table_name = 'user'


if __name__ == "__main__":
    db.connect()
    db.create_tables([User])

    # 批量插入
    users = [{"name": f"root{i}"} for i in range(5)]
    User.insert_many(users).execute()
    users = [{"name": f"root{i}"} for i in range(3, 10)]
    User.insert_many(users).execute()

    # 原始
    query = User.select()
    for u in query:
        print(u.name)
    print("=============")

    # 去重
    query = User.select().distinct()
    for u in query:
        print(u.name)
    print("=============")

    # 统计
    print(User.select().distinct().count())

    # 删除表，要先删除外键
    db.drop_tables([User])
