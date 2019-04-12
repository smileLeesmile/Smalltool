from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql,os,json
import sqlite3

from pymysql import IntegrityError
from sqlalchemy import or_, func

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# #为app配置数据库的配置信息
base_dir=os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]='mysql://root:123456@localhost:3306/flask'
# app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///'+os.path.join(base_dir,"flask.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#Z指定当师视图执行完毕后，自动提交到数据库
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
#执行玩语句后自动执行打印原始的sql语句
app.config['SQLALCHEMY_ECHO']=True
#创建SQLAlchemy的数据库实例
db = SQLAlchemy(app)

class Permission(db.Model):
    __tablename__= 'permission'
    version = db.Column(db.String(100),nullable=False)
    authoritynumber = db.Column(db.String(100), primary_key=True,unique=True)
    # authoritynumber = db.Column(db.String(100), unique=True)
    applyuser = db.Column(db.String(80),nullable=False)
    changetype = db.Column(db.String(80),nullable=False)
    authoritytype=db.Column(db.String(120),nullable=False)
    rootnode=db.Column(db.String(100),nullable=False)
    rootname = db.Column(db.String(100), nullable=False)
    authorityname = db.Column(db.String(100), nullable=False)
    authoritydescription = db.Column(db.String(100), nullable=False)
    guioperateentrance = db.Column(db.String(100), nullable=False)
    dependecy = db.Column(db.String(100), nullable=False)
    userimpact=db.Column(db.String(100),nullable=False)

    def __init__(self,version,authoritynumber,applyuser,changetype,authoritytype,rootnode, rootname,authorityname,authoritydescription,guioperateentrance,dependecy,userimpact):
        self.version=version
        self.authoritynumber = authoritynumber
        self.applyuser = applyuser
        self.changetype = changetype
        self.authoritytype = authoritytype
        self.rootnode = rootnode
        self.rootname = rootname
        self.authorityname = authorityname
        self.authoritydescription = authoritydescription
        self.guioperateentrance = guioperateentrance
        self.dependecy = dependecy
        self.userimpact = userimpact

    # def __repr__(self):
    #     return '<Users:%r>'% self.username

# 将创建好的实体类映射回数据库
db.create_all()

@app.route('/01-index',methods=['GET','POST'])
def index_views():
    print("跳转首页成功")
    return  render_template("01-index.html")    #响应一下use

@app.route('/02zn-add',methods=['GET','POST'])
def zn_view():
    if request.method == 'GET':
        return  render_template('02zn-add.html')
    else:
        #接收前端传递过来的数据
        version=request.form.get('version')
        authoritynumber=request.form.get('authoritynumber')
        applyuser=request.form.get('applyuser')
        changetype = request.form.get('changetype')
        authoritytype = request.form.get('authoritytype')
        rootnode = request.form.get('rootnode')
        rootname = request.form.get('rootname')
        authorityname = request.form.get('authorityname')
        authoritydescription = request.form.get('authoritydescription')
        guioperateentrance = request.form.get('guioperateentrance')
        dependecy = request.form.get('dependecy')
        userimpact = request.form.get('userimpact')
        print(version,authoritynumber,applyuser,changetype,authoritytype,rootnode,rootname,authorityname,authoritydescription,guioperateentrance,dependecy,userimpact)
        #将数据构建成实体对象
        permission=Permission(version,authoritynumber,applyuser,changetype,authoritytype,rootnode,rootname,authorityname,authoritydescription,guioperateentrance,dependecy,userimpact)
        #将数据保存会数据库
        try:
            db.session.add(permission)
            db.session.commit()
            # flash("添加成功")
        except Exception as e:
            print(e)
            db.session.rollback()
            print("12312")
            # flash("添加失败")
        # return "Register Success"
        return render_template("ceshicuowu.html")


@app.route('/02en-add',methods=['GET','POST'])
def en_view():
    if request.method == 'GET':
        return  render_template('02en-add.html')
    else:
        #接收前端传递过来的数据
        version=request.form.get('version')
        authoritynumber=request.form.get('authoritynumber')
        applyuser=request.form.get('applyuser')
        changetype = request.form.get('changetype')
        authoritytype = request.form.get('authoritytype')
        rootnode = request.form.get('rootnode')
        rootname = request.form.get('rootname')
        authorityname = request.form.get('authorityname')
        authoritydescription = request.form.get('authoritydescription')
        guioperateentrance = request.form.get('guioperateentrance')
        dependecy = request.form.get('dependecy')
        userimpact = request.form.get('userimpact')
        print(version,authoritynumber,applyuser,changetype,authoritytype,rootnode,rootname,authorityname,authoritydescription,guioperateentrance,dependecy,userimpact)
        #将数据构建成实体对象
        permission=Permission(version,authoritynumber,applyuser,changetype,authoritytype,rootnode,rootname,authorityname,authoritydescription,guioperateentrance,dependecy,userimpact)
        #将数据保存会数据库
        try:
            db.session.add(permission)
            db.session.commit()
            # flash("添加成功")
        except IntegrityError as e:
            print(e)
            # flash("添加失败")
        # return "Register Success"
        finally:
            return render_template("ceshicuowu.html")

@app.route('/03-query',methods=['GET','POST'])
def query_views():
    if request.method == 'GET':
        return render_template('03-condition.html')
    else:
        version1 = request.form.get('version')
        authoritynumber2 = request.form.get('authoritynumber')
        #查询结果对象
        permission=Permission.query.filter(or_(Permission.version==version1,Permission.authoritynumber==authoritynumber2))
        print(permission)
        return render_template("03-result.html",rs=permission)


@app.route('/04-update',methods=['GET','POST'])
def queryall_view3():
    if request.method == 'GET':
        id = request.args.get('id')
        id1=request.args.get('id1')
        print(id)
        user1=Permission.query.filter(Permission.authoritynumber==id)
        print(id1,type(id1))
        print(id1.isalpha())
        if id1.encode().isalpha():
            return render_template('04en-update.html', mess=user1)
        else:
            return render_template('04zn-update.html', mess=user1)
    else:
        ff=request.form.get('authoritynumber')
        # 接收前端传递过来的数据
        permission=Permission.query.filter(Permission.authoritynumber==ff).first()
        permission.version = request.form.get('version')
        permission.authoritynumber = ff
        permission.applyuser = request.form.get('applyuser')
        permission.changetype = request.form.get('changetype')
        permission.authoritytype = request.form.get('authoritytype')
        permission.rootnode = request.form.get('rootnode')
        permission.rootname = request.form.get('rootname')
        permission.authorityname = request.form.get('authorityname')
        permission.authoritydescription = request.form.get('authoritydescription')
        permission.guioperateentrance = request.form.get('guioperateentrance')
        permission.dependecy = request.form.get('dependecy')
        permission.userimpact = request.form.get('userimpact')
        print(permission.version, permission.authoritynumber,permission.applyuser,permission.changetype, permission.authoritytype,permission.rootnode,permission.rootname,permission.authorityname,permission.authoritydescription,permission.guioperateentrance,permission.dependecy,permission.userimpact)
        db.session.add(permission)
        db.session.commit()
        return render_template("ceshi.html")

@app.route('/05-delete')
def delate_view2():
    id=request.args.get('id')
    user=Permission.query.filter(Permission.authoritynumber==id).first()

    db.session.delete(user)
    return  render_template("ceshi.html")

if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1')