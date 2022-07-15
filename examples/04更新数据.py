import datetime
from email.policy import default

from zdppy_orm import *
import logging

# 创建日志对象
logger = logging.getLogger("zdppy_orm")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# 创建数据库连接
db = MySQLDatabase('zdppy_orm', host='127.0.0.1', user='root', passwd='root')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = TextField()
    age = IntegerField(default=0)

    class Meta:
        table_name = 'user'


class Tweet(BaseModel):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref="tweets")

    class Meta:
        table_name = 'tweet'


class Favorite(BaseModel):
    user = ForeignKeyField(User, backref="favorites")
    tweet = ForeignKeyField(Tweet, backref="favorites")


if __name__ == "__main__":
    db.connect()
    db.create_tables([User, Tweet, Favorite])

    # 创建
    User.create(username="zhangsan")
    User.create(username="lisi")

    # 更新
    charlie = User(username="charlie")  # update set xx=xx where username="charlie"
    print(charlie.save())
    charlie.name = "张大鹏"
    charlie.save()

    # 使用update更新
    print(User.update(age=20).where(User.username == "lisi").execute())

    # 删除表，要先删除外键
    db.drop_tables([Favorite, Tweet, User])
