from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import time

# 以下都是套路
app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 指定数据库的路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weibos.db'

db = SQLAlchemy(app)

def format_time(t):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(t)
    dt = time.strftime(format, value)
    return dt
# 定义一个 Model，继承自 db.Modelhttp://vip.cocode.cc/chest/shared/1657
class Weibo(db.Model):
    __tablename__ = 'weibos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    username = db.Column(db.String())


    def __repr__(self):
        return u'<ToDo {} {}>'.format(self.id, self.content)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = format_time(int(time.time()))
        self.username = 'by:' + form.get('username', '')

    def valid(self):
        return len(self.content) > 0


class Comment(db.Model):
    __tablename__ = 'comments'
    # 下面是字段定义
    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    weibo_id = db.Column(db.Integer)


    def __repr__(self):
        return u'<{} {}>'.format(self.content, self.created_time)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = format_time(int(time.time()))
        self.weibo_id = form.get('weibo_id', '')

    def valid(self):
        return len(self.content) > 0

class User(db.Model):
    __tablename__ = 'users'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    def __repr__(self):
        return u'<User {} {}>'.format(self.id, self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = format_time(int(time.time()))

    def valid(self):
        return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False


if __name__ == '__main__':
    # 先 drop_all 删除所有数据库中的表
    # 再 create_all 创建所有的表
    db.drop_all()
    db.create_all()
    print('rebuild database')
