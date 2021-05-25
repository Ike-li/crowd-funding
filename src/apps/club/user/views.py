import functools
import uuid
import time
from datetime import datetime

import cassandra.util
from flask import Blueprint, session, render_template, request, flash, redirect, url_for

from src.apps.settings import cass_session

user_bp = Blueprint('user', __name__)


# 加载用户 session 的装饰器，检查需要用到与用户 session 相关的视图函数
def load_user(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if not session.get('user_name'):
            return render_template('user/sign.html', msg='请登录!')
        return func(*args, **kwargs)

    return inner


# 从 session 获取 user_name
def load_user_name():
    user_name = session.get('user_name')
    return user_name


# 模板全局变量 user_name
@user_bp.app_context_processor
def get_current_user():
    user_name = load_user_name()
    return dict(user_name=user_name)


@user_bp.route('/registering')
def user_registering():
    return render_template('user/register.html')


# 用户注册
@user_bp.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('user/register.html')
    # 接受收表单提交过来的参数
    user_name = request.form.get('user_name')
    user_passwd = request.form.get('user_passwd')
    user_email = request.form.get('email')
    user_phone = request.form.get('phone')
    ls = [user_name]
    ls1 = [user_phone]
    ls2 = [user_email]
    ls3 = [user_name, 500, user_email, user_passwd, user_phone]
    cql = "SELECT user_name FROM users.user WHERE user_name = %s;"
    if len(cass_session.execute(cql, ls).all()) != 0:
        flash("该用户名已被注册")
        return render_template('user/register.html')
    elif len((cass_session.execute("SELECT user_phone FROM users.user WHERE user_phone = %s;", ls1)).all()) != 0:
        flash("手机号已被注册")
        return render_template('user/register.html')
    elif len((cass_session.execute("SELECT user_email FROM users.user WHERE user_email = %s;", ls2)).all()) != 0:
        flash("邮箱已被注册")
        return render_template('user/register.html')
    else:
        cass_session.execute(
            "INSERT "
            "INTO users.user (user_name,user_account,user_email, user_passwd,user_phone)"
            "VALUES (%s, %s, %s, %s, %s);",
            ls3)
        flash("注册成功")
        return redirect(url_for('user.user_logging'))


# 用户主页
@user_bp.route('/user')
@load_user
def user_center():
    print(session)
    print(session['user_name'])
    cass_ls = [session['user_name']]
    cql = "SELECT * FROM users.user WHERE user_name = %s;"
    data = cass_session.execute(cql, cass_ls).all()
    print(type(data[0]))
    return render_template('user_info.html', parameter=data[0])


# 用户登录界面
@user_bp.route('/logging')
@load_user
def user_logging():
    return render_template('user/sign.html')


# 用户登录
@user_bp.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return render_template('user/sign.html')
    # 接受收表单提交过来的参数
    user_name = request.form.get('user_name')
    user_passwd = request.form.get('user_passwd')
    # 根据用户名在数据库比对用户信息的合法性
    cass_ls = [user_name]
    cql = "SELECT * FROM users.user WHERE user_name = %s;"

    # 判断用户是否存在
    if len(cass_session.execute(cql, cass_ls).all()) == 0:
        return render_template('user/sign.html', msg='该用户不存在!')

    # 如果用户存在则对比密码是否相等
    cql1 = "SELECT user_passwd FROM users.user WHERE user_name = %s;"
    cass_get_data = cass_session.execute(cql1, cass_ls)

    for rows in cass_get_data:
        if user_passwd == rows['user_passwd']:
            session['user_name'] = user_name
            session.permanent = True  # 在用户登陆成功代码设置 session 持续时间为 True
            flash("欢迎回来！" + user_name)
            return redirect(url_for('index'))  # 重定向时要带上蓝图的名字.函数名
        else:
            return render_template('user/sign.html', msg='用户名或密码错误!')


# 用户注销
@user_bp.route('/logout')
@load_user
def user_logout():
    session.pop('user_name')
    flash("注销成功")
    return redirect(url_for('index'))


# 任务添加
@user_bp.route('/add')
@load_user
def add_function():
    return render_template('user/create_new_function.html')


# 用户任务添加
@user_bp.route('/add_function', methods=['POST'])
@load_user
def user_add_function():
    function_id = cassandra.util.uuid_from_time(time.time())  # id
    function_content = request.form.get('content')
    comments = request.form.get('comments')
    created_at = datetime.now()  # 创建时间
    function_type = request.form.get('type')  # 类型
    crowd_funding_days = int(request.form.get('days'))  # 众筹时间
    crowd_funding_money = int(request.form.get('money'))  # 众筹金额
    function_introduction = request.form.get('introduction')  # 简介
    function_title = request.form.get('title')  # 标题
    function_cover = request.form.get('cover')  # 封面
    # country = request.form.get('country')
    # province = request.form.get('province')
    # city = request.form.get('city')
    # street = request.form.get('street')
    # code = request.form.get('code')
    publisher = session.get('user_name')
    state = "未审核"
    # 添加 FR 到 functions.functions_request
    ls = [function_id, comments, created_at, crowd_funding_days, crowd_funding_money, function_content, function_cover,
          function_introduction, function_title, function_type, publisher, state]
    cql = "INSERT INTO functions.functions_request (function_id, comments, created_at, crowd_funding_days, " \
          "crowd_funding_money, function_content, function_cover, function_introduction, function_title, " \
          "function_type, publisher, state) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cass_session.execute(cql, ls)

    # 添加 FR 到 functions_request_by_status
    ls1 = [state, function_id, created_at, function_title, function_type, publisher]
    cql1 = "INSERT  INTO functions.functions_request_by_status (state, function_id, created_at, function_title, " \
           "function_type, publisher) VALUES (%s,%s,%s,%s,%s,%s);"
    cass_session.execute(cql1, ls1)

    # 添加任务到 user.user_by_publish
    ls2 = [publisher, function_id, created_at, function_title, function_type, state]
    cql2 = "INSERT INTO users.user_by_publish (user_name, function_id, create_at, function_title, function_type, " \
           "state) VALUES (%s,%s,%s,%s,%s,%s);"
    cass_session.execute(cql2, ls2)
    flash("添加任务成功！")
    return render_template('index.html')


# 用户查看自己所有 已发布 / 未审核 / 审核中 / 未通过的 FR
@user_bp.route('/user_functions/<state>')
@load_user
def user_functions(state):
    ls = [session.get('user_name'), state]
    cql = "SELECT * FROM users.user_by_publish WHERE user_name = %s AND state = %s ALLOW FILTERING;"
    data = cass_session.execute(cql, ls)
    ls1 = data.all()
    return render_template('user/user_functions.html', args=ls1, status=state)


# 用户查看自己某一个已发布的 FR
@user_bp.route('/function_published/<function_id>')
@load_user
def function_published_one(function_id):
    ls = [uuid.UUID(function_id)]
    cql = "SELECT * FROM functions.functions WHERE function_id = %s;"
    data = cass_session.execute(cql, ls)
    ls1 = data.all()
    return render_template('user/user_published_one.html', args=ls1)


# 用户查查看自己某一个 未审核 / 审核中 / 未通过 的 FR
@user_bp.route('/function_unpublished/<function_id>')
@load_user
def function_unpublished_one(function_id):
    ls = [uuid.UUID(function_id)]
    cql = "SELECT * FROM functions.functions_request WHERE function_id = %s; "
    data = cass_session.execute(cql, ls)
    ls1 = data.all()
    return render_template('user/user_unpublished_one.html', args=ls1)
