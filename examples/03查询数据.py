import datetime

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

    User.create(username="zhangsan")
    User.create(username="lisi")

    # 3. 查询
    # 1. get方法 - 1. 返回来的是直接的user对象 2. 这个方法如果查询不到会抛出异常
    try:
        charlie = User.get(User.username == "charie")
        print(charlie.username)

        charlie = User.get_by_id("charie")
        print(charlie.username)
        # 这个操作发起的sql请求是什么
    except User.DoesNotExist as e:
        print("查询不到")

    # 2. 查询所有
    users = User.select()
    print(users.sql())
    print(type(users))
    user = users[0]
    print(type(user))

    usernames = ["charlie", "huey", "mickey"]
    users = User.select().where(User.username.in_(usernames))
    for user in users:
        print(user.username)
    for user in User.select():
        print(user.username)

    # 删除
    db.drop_tables([Favorite, Tweet, User])
