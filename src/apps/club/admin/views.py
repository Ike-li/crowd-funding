import functools
import uuid
from datetime import datetime, timedelta

from flask import Blueprint, request, render_template, redirect, url_for, session, flash

from src.apps.settings import cass_session

# 创建蓝图对象 admin_bp
admin_bp = Blueprint('admin', __name__)


# 加载管理员 session 的装饰器，检查需要用到与管理员 session 相关的视图函数
def load_admin(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if not session.get('admin_name'):
            return render_template('admin/admin_login.html', msg='请登录!')
        return func(*args, **kwargs)

    return inner


# 从 session 获取 admin_name
def load_admin_name():
    admin_name = session.get('admin_name')
    return admin_name


# 模板全局变量 admin_name
@admin_bp.app_context_processor
def get_current_admin():
    admin_name = load_admin_name()
    return dict(admin_name=admin_name)


# 管理员主页
@admin_bp.route('/')
@load_admin
def admin_center():
    cql = "SELECT * " \
          "FROM functions.functions_request_by_status " \
          "WHERE state = '未审核';"
    data = cass_session.execute(cql)
    functions_request = data.all()
    return render_template('admin/admin_info.html', args=functions_request, state="未审核")


# 管理员登录界面
@admin_bp.route('/logging')
@load_admin
def admin_logging():
    return render_template('admin/admin_login.html')


# 管理员登陆检查
@admin_bp.route('/login', methods=['GET', "POST"])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/admin_login.html')
    # 接受收表单提交过来的参数
    admin_name = request.form.get('admin_name')
    admin_passwd = request.form.get('admin_passwd')
    # 根据用户名在数据库比对用户信息的合法性
    cass_ls = [admin_name]
    cql = "SELECT * " \
          "FROM functions.admin " \
          "WHERE admin_name = %s;"

    # 判断管理员是否存在
    if len(cass_session.execute(cql, cass_ls).all()) == 0:
        return render_template('admin/admin_login.html', msg='该管理员不存在!')

    # 如果管理员存在则对比密码是否相等
    cql1 = "SELECT admin_passwd " \
           "FROM functions.admin " \
           "WHERE admin_name = %s;"
    cass_get_data = cass_session.execute(cql1, cass_ls)

    for rows in cass_get_data:
        # if admin_name and admin_passwd == admin_passwd['admin_passwd']:
        if admin_passwd == rows['admin_passwd']:
            session['admin_name'] = admin_name
            session.permanent = True  # 在用户登陆成功代码设置 session 持续时间为 True
            flash("欢迎回来！" + admin_name)
            return redirect(url_for('admin.admin_center'))  # 重定向时要带上蓝图的名字.函数名
        else:
            return render_template('admin/admin_login.html', msg='用户名或密码错误!')


# 管理员注销
@admin_bp.route('/logout')
@load_admin
def admin_logout():
    session.pop('admin_name')
    flash("注销成功")
    return redirect(url_for('index', ))


# 管理员查看审核表各功能的状态
@admin_bp.route('/functions')
@load_admin
def functions_state():
    """
    返回check_list的 部分FR(仅包含未审核、已通过、审核中、未通过四种)
    :return:
    """

    state = request.args.get('state')
    ls = [state]
    cql = "SELECT * " \
          "FROM functions.functions_request_by_status " \
          "WHERE state = %s; "
    data = cass_session.execute(cql, ls)
    functions = data.all()
    print(functions)
    # ls1 = []
    # for i in data:
    #     ls1.append(i)
    if state == "未审核":
        return render_template('admin/admin_functions_not_reviewed.html', args=functions, state=state)
    elif state == "审核中":
        return render_template('admin/admin_functions_under_review.html', args=functions, state=state)
    elif state == "未通过":
        return render_template('admin/admin_functions_under_review.html', args=functions, state=state)
    elif state == "已通过":
        return render_template('admin/admin_functions_under_review.html', args=functions, state=state)
    else:
        # return render_template('404.html')
        return "Failed"


# 管理员查看某请求任务的详细信息
@admin_bp.route('/<function_id>', methods=['GET'])
@load_admin
def function(function_id):
    ls = [uuid.UUID(function_id)]
    cql = "SELECT * " \
          "FROM functions.functions_request " \
          "WHERE function_id = %s;"
    data = cass_session.execute(cql, ls)
    functions_request = data.all()
    return render_template('admin/admin_functions_update.html', args=functions_request)


# 管理员更新某功能的状态
@admin_bp.route('/update', methods=['POST'])
@load_admin
def check_function():
    state = request.form.get('state')
    stated = request.form.get('stated')
    comments = request.form.get('comments')
    function_id = uuid.UUID(request.form.get('function_id'))
    ls = [comments, state, function_id]
    print(ls)

    # 更新 functions.functions_request 的状态
    cql = "UPDATE functions.functions_request " \
          "SET comments = %s, state = %s " \
          "WHERE function_id = %s;"
    cass_session.execute(cql, ls)

    # 删除 functions.functions_request_by_status 的对应记录，因为 state为主键不能修改
    ls1 = [stated, function_id]
    cql1 = "DELETE FROM functions.functions_request_by_status " \
           "WHERE state = %s " \
           "AND function_id = %s;"
    cass_session.execute(cql1, ls1)

    # 查询出该条记录的其他 字段，为删除再插入 functions.functions_request_by_status 表到作准备
    ls2 = [function_id]
    cql2 = "SELECT function_type,function_title,publisher, created_at " \
           "FROM functions.functions_request " \
           "WHERE function_id = %s "
    data = cass_session.execute(cql2, ls2)

    ls3 = data.all()

    # 插入修改后的记录进 functions.functions_request_by_status表
    ls4 = [state, function_id, ls3[0].get('created_at'), ls3[0].get('function_title'), ls3[0].get('function_type'),
           ls3[0].get('publisher')]
    print(ls4)
    cql4 = "INSERT INTO functions.functions_request_by_status " \
           "(state, function_id, created_at, function_title, function_type, publisher) " \
           "VALUES (%s, %s,%s, %s, %s, %s); "
    cass_session.execute(cql4, ls4)

    # 更新 user.user_by_publish 的旧记录 里的 state

    ls10 = [state, ls3[0].get('publisher'), function_id, ls3[0].get('created_at')]
    cql10 = "UPDATE users.user_by_publish " \
            "SET state = %s " \
            "WHERE user_name = %s " \
            "AND function_id = %s " \
            "AND create_at = %s;"
    cass_session.execute(cql10, ls10)

    # FR 通过的操作
    if state == "已通过":
        # 查询 functions.functions_request 审核已通过的 FR
        ls5 = [function_id]
        cql5 = "SELECT * " \
               "FROM functions.functions_request " \
               "WHERE function_id = %s;"
        data = cass_session.execute(cql5, ls5)
        function_by_request = data.all()[0]
        created_at = datetime.now()
        closing_time = created_at + timedelta(function_by_request['crowd_funding_days'])
        created_at_date = (datetime.now()).date()

        # 插入到 function 表实现在广场开始众筹
        ls6 = [function_id, closing_time, created_at, created_at_date, 0, function_by_request['crowd_funding_days'],
               function_by_request['crowd_funding_money'], function_by_request['function_content'],
               function_by_request['function_cover'], function_by_request['function_introduction'],
               function_by_request['function_title'], function_by_request['function_type'],
               function_by_request['publisher'], function_by_request['state']]
        cql6 = "INSERT INTO functions.functions " \
               "(function_id, closing_time, created_at, created_at_date," \
               "crowd_funding_current_money, crowd_funding_days, crowd_funding_money, function_content, " \
               "function_cover, function_introduction, function_title, function_type, publisher, state) " \
               "VALUES (%s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cass_session.execute(cql6, ls6)

        # 添加任务的 function_by_type
        ls7 = [function_by_request['function_type'], function_by_request['function_id'],
               function_by_request['crowd_funding_money'], function_by_request['function_cover'],
               function_by_request['function_introduction'], function_by_request['function_title'],
               function_by_request['publisher']]
        cql7 = "INSERT INTO functions.functions_by_type " \
               "(function_type, function_id, crowd_funding_money, function_cover, function_introduction, " \
               "function_title, publisher) " \
               "VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cass_session.execute(cql7, ls7)

        # 添加任务到 function_by_time
        ls8 = [created_at.date(), function_by_request['function_id'], function_by_request['crowd_funding_money'],
               function_by_request['function_cover'], function_by_request['function_introduction'],
               function_by_request['function_title'], function_by_request['function_type'],
               function_by_request['publisher']]
        cql8 = "INSERT INTO functions.functions_by_time " \
               "(created_at, function_id, crowd_funding_money, function_cover, function_introduction, " \
               "function_title, function_type, publisher) " \
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        cass_session.execute(cql8, ls8)

        # 删除 user_by_publish 的旧纪录
        ls13 = [function_by_request['publisher'], function_id]
        cql13 = "DELETE FROM users.user_by_publish" \
                " WHERE user_name = %s " \
                "AND function_id = %s;"
        cass_session.execute(cql13, ls13)

        # 添加 FR 到 user_by_publish
        ls9 = [function_by_request['publisher'], function_by_request['function_id'], created_at,
               function_by_request['function_title'], function_by_request['function_type'], state]
        cql9 = "INSERT INTO users.user_by_publish" \
               "(user_name, function_id, create_at, function_title, function_type, state) " \
               "VALUES (%s, %s, %s, %s, %s, %s)"
        cass_session.execute(cql9, ls9)

    flash("更新成功!")
    return redirect(url_for('admin.functions_state', state=state))


# 管理员查看各功能收藏统计
@admin_bp.route('/all_functions_collections', methods=['GET'])
@load_admin
def show_all_collections():
    all_functions_collections_cql = "SELECT function_id,function_title,collections " \
                                    "FROM functions.functions_collections_counter;"
    all_functions_collections__rows = cass_session.execute(all_functions_collections_cql)
    collection = all_functions_collections__rows.all()
    return render_template('admin/admin_all_functions_collections.html', collectiion=collection)


# 管理员查看单个功能的收藏统计
@admin_bp.route('/collections/<function_id>', methods=['GET', 'POST'])
@load_admin
def show_one_collections(function_id):
    ls = [uuid.UUID(function_id)]
    cql = "SELECT * " \
          "FROM functions.functions_collections " \
          "WHERE function_id = %s;"
    data = cass_session.execute(cql, ls)
    collections = data.all()
    return render_template('admin/admin_one_functions_collections.html', collections=collections)


# 管理员查看所有用户
@admin_bp.route('/users', methods=['GET'])
@load_admin
def show_all_users():
    cql = "SELECT user_name,user_account,user_phone " \
          "FROM users.user;"
    data = cass_session.execute(cql)
    users = data.all()
    return render_template('admin/admin_users_info.html', users=users)


# 管理员查看众筹成功的 Fr
@admin_bp.route('/crowd-funding_success')
@load_admin
def show_crowd_funding_success_functions():
    success_functions_cql = "SELECT * " \
                            "FROM functions.success_functions;"
    success_functions_rows = cass_session.execute(success_functions_cql)
    success_functions = success_functions_rows.all()
    return render_template('admin/admin_success_functions.html', success_functions=success_functions)


# 管理员查看众筹失败的 Fr
@admin_bp.route('/crowd-funding_fail')
@load_admin
def show_crowd_funding_fail_functions():
    fail_functions_cql = "SELECT * " \
                         "FROM functions.fail_functions;"
    fail_functions_rows = cass_session.execute(fail_functions_cql)
    fail_functions = fail_functions_rows.all()
    return render_template('admin/admin_fail_functions.html', fail_functions=fail_functions)


@admin_bp.route('/all_functions_collections')
@load_admin
def all_functions_donations():
    all_functions_donations_cql = "SELECT * " \
                                  "FROM functions.functions_contribution;"
    all_functions_donations_rows = cass_session.execute(all_functions_donations_cql)
    all_functions_donations_data = all_functions_donations_rows.all()
    return render_template('admin/admin_all_functions_donations.html',
                           all_functions_donations=all_functions_donations_data)
