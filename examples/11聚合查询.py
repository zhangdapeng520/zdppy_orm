import datetime

from zdppy_orm import *
import logging

logger = logging.getLogger("zdppy_orm")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

db = MySQLDatabase('zdppy_orm', host='127.0.0.1', user='root', passwd='root')


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.datetime.now, verbose_name="添加时间")

    class Meta:
        database = db  # 这里是数据库链接，为了方便建立多个表，可以把这个部分提炼出来形成一个新的类


class User(BaseModel):
    # 如果没有设置主键，那么自动生成一个id的主键
    username = CharField(max_length=20)
    age = CharField(default=18, max_length=20, verbose_name="年龄")

    class Meta:
        table_name = 'new_user'  # 这里可以自定义表名


if __name__ == "__main__":
    db.connect()
    db.create_tables([User])

    users = [{"username": f"root{i}", "age": i} for i in range(100)]
    User.insert_many(users).execute()

    # select user.name from user where age=(select max(age) from user)
    max_age = User.select(fn.MAX(User.age)).scalar()
    print(max_age)
    users = User.select().where(User.age == max_age)
    for user in users:
        print(user.username, user.age)

    db.drop_tables([User])
