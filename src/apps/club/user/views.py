import functools
import os
import uuid
import time
from datetime import datetime

import cassandra.util
from flask import Blueprint, session, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from src.apps.settings import cass_session

user_bp = Blueprint('user', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'src/apps/static/user_images'


# 加载用户 session 的装饰器，检查需要用到与用户 session 相关的视图函数
def load_user(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        if not session.get('user_name'):
            return render_template('user/sign.html', msg='请登录!')
        return func(*args, **kwargs)

    return inner


# 允许的图片后缀格式
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 从 session 获取 user_name
def load_user_name():
    user_name = session.get('user_name')
    return user_name


# 模板全局变量 user_name
@user_bp.app_context_processor
def get_current_user():
    # user_account = None
    user_name = load_user_name()
    if user_name is None:
        user_account = 0
    else:
        user_account_query_list = [user_name]
        user_account_query_cql = "SELECT user_account " \
                                 "FROM users.user " \
                                 "WHERE user_name = %s;"
        account_rows = cass_session.execute(user_account_query_cql, user_account_query_list)
        user_account = account_rows.all()[0].get('user_account')

    return dict(user_name=user_name, user_account=user_account)


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
    cql = "SELECT user_name " \
          "FROM users.user " \
          "WHERE user_name = %s;"
    if len(cass_session.execute(cql, ls).all()) != 0:
        flash("该用户名已被注册")
        return render_template('user/register.html')
    elif len((cass_session.execute("SELECT user_phone "
                                   "FROM users.user "
                                   "WHERE user_phone = %s;", ls1)).all()) != 0:
        flash("手机号已被注册")
        return render_template('user/register.html')
    elif len((cass_session.execute("SELECT user_email "
                                   "FROM users.user "
                                   "WHERE user_email = %s;", ls2)).all()) != 0:
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
    ls = [session.get('user_name'), "已通过"]
    cql = "SELECT * " \
          "FROM users.user_by_publish " \
          "WHERE user_name = %s " \
          "AND state = %s " \
          "ALLOW FILTERING;"
    rows = cass_session.execute(cql, ls)
    functions = rows.all()
    return render_template('user/user_info.html', args=functions, state="已通过")


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
    cql = "SELECT * " \
          "FROM users.user " \
          "WHERE user_name = %s;"
    # cql = "select * from users.user where user_name in (%s);"

    # 判断用户是否存在
    if len(cass_session.execute(cql, cass_ls).all()) == 0:
        return render_template('user/sign.html', msg='该用户不存在!')

    # 如果用户存在则对比密码是否相等
    cql1 = "SELECT user_passwd " \
           "FROM users.user " \
           "WHERE user_name = %s;"
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
    new_file_name = None
    if request.method == 'POST':
        file = request.files['function-cover']
        if not (file and allowed_file(file.filename)):
            flash("图片上传不符合规则")
            return render_template('user/create_new_function.html')
        base_path = os.path.dirname(__file__)  # 当前文件所在路径
        new_file_name = f"{cassandra.util.uuid_from_time(time.time())}.jpg"
        upload_path = os.path.join(base_path, '../../static/user_images', secure_filename(new_file_name))  # 重命名图片名
        file.save(upload_path)
    function_cover = '../../static/user_images/' + new_file_name  # 封面路径
    function_id = cassandra.util.uuid_from_time(time.time())  # id
    function_content = request.form.get('content')
    created_at = datetime.now()  # 创建时间
    function_type = request.form.get('type')  # 类型
    crowd_funding_days = int(request.form.get('days'))  # 众筹时间
    crowd_funding_money = int(request.form.get('money'))  # 众筹金额
    function_introduction = request.form.get('introduction')  # 简介
    function_title = request.form.get('title')  # 标题
    publisher = session.get('user_name')
    state = "未审核"
    comments = None
    # 添加 FR 到 functions.functions_request
    ls = [function_id, comments, created_at, crowd_funding_days, crowd_funding_money, function_content, function_cover,
          function_introduction, function_title, function_type, publisher, state]
    cql = "INSERT INTO functions.functions_request " \
          "(function_id, comments, created_at, crowd_funding_days, " \
          "crowd_funding_money, function_content, function_cover, function_introduction, function_title, " \
          "function_type, publisher, state) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    cass_session.execute(cql, ls)

    # 添加 FR 到 functions_request_by_status
    ls1 = [state, function_id, created_at, function_title, function_type, publisher]
    cql1 = "INSERT  INTO functions.functions_request_by_status " \
           "(state, function_id, created_at, function_title, function_type, publisher) " \
           "VALUES (%s,%s,%s,%s,%s,%s);"
    cass_session.execute(cql1, ls1)

    # 添加任务到 user.user_by_publish
    ls2 = [publisher, function_id, created_at, function_title, function_type, state]
    cql2 = "INSERT INTO users.user_by_publish " \
           "(user_name, function_id, create_at, function_title, function_type, state) " \
           "VALUES (%s,%s,%s,%s,%s,%s);"
    cass_session.execute(cql2, ls2)
    flash("添加任务成功！")
    return redirect(url_for('index'))


# 用户查看自己所有 已发布 / 未审核 / 审核中 / 未通过的 FR
@user_bp.route('/user_functions/<state>')
@load_user
def user_functions(state):
    ls = [session.get('user_name'), state]
    cql = "SELECT * " \
          "FROM users.user_by_publish " \
          "WHERE user_name = %s " \
          "AND state = %s " \
          "ALLOW FILTERING;"
    data = cass_session.execute(cql, ls)
    functions = data.all()
    if state == "已通过":
        return render_template('user/user_functions_published.html', args=functions, state=state)
    elif state == "审核中":
        return render_template('user/user_functions_under_review.html', args=functions, state=state)
    elif state == "未通过":
        return render_template('user/user_functions_failed.html', args=functions, state=state)
    elif state == "未审核":
        return render_template('user/user_functions_not_reviewed.html', args=functions, state=state)
    else:
        # return render_template('404.html')
        return "Failed"


# 用户查看自己某一个已发布的 FR
@user_bp.route('/function_published/<function_id>')
@load_user
def function_published_one(function_id):
    function_published_list = [uuid.UUID(function_id)]
    function_published_cql = "SELECT * " \
                             "FROM functions.functions " \
                             "WHERE function_id = %s;"
    function_published_data = cass_session.execute(function_published_cql, function_published_list)
    function_published_details = function_published_data.all()
    return render_template('user/user_function_published_details.html', args=function_published_details)


# 用户查看自己某一个 未审核 / 审核中 / 未通过 的 FR
@user_bp.route('/function_unpublished/<function_id>')
@load_user
def function_unpublished_one(function_id):
    function_unpublished_id = [uuid.UUID(function_id)]
    function_unpublished_cql = "SELECT * " \
                               "FROM functions.functions_request " \
                               "WHERE function_id = %s;"
    function_unpublished_data = cass_session.execute(function_unpublished_cql, function_unpublished_id)
    function_unpublished_details = function_unpublished_data.all()
    if function_unpublished_details[0].get('state') == "未审核":
        return render_template('user/user_function_not_reviewed_details.html', args=function_unpublished_details)
    return render_template('user/user_function_unpublished_details.html', args=function_unpublished_details)


# 用户查看自己的打赏的任务
@user_bp.route('/my_donations')
@load_user
def my_donations():
    user_donate_list = [session.get('user_name')]
    # 用户对该 FR 的打赏
    user_donate_cql = "SELECT * " \
                      "FROM users.user_by_contribution " \
                      "WHERE user_name = %s;"
    user_donate_rows = cass_session.execute(user_donate_cql, user_donate_list)
    functions = user_donate_rows.all()
    # # 所有玩家对 此 FR 的打赏
    # function_id = functions[0].get('function_id')
    # all_donate_list = [function_id]
    # all_donate_cql = "SELECT crowd_funding_current_money FROM functions.functions WHERE function_id = %s;"
    # all_donate_rows = cass_session.execute(all_donate_cql, all_donate_list)
    # all_donate = all_donate_rows.all()[0].get('crowd_funding_current_money')

    return render_template('user/my_donations.html', args=functions, state="我的打赏")


# 用户查看自己的收藏
@user_bp.route('/my_collections')
@load_user
def my_collections():
    ls = [session.get('user_name')]
    cql = "SELECT * " \
          "FROM users.user_by_collection " \
          "WHERE user_name = %s;"
    rows = cass_session.execute(cql, ls)
    functions = rows.all()
    return render_template('user/my_collections.html', args=functions, state="我的收藏")


# 用户查看自己的评论
@user_bp.route('/my_comments')
@load_user
def my_comments():
    ls = [session.get('user_name')]
    cql = "SELECT * " \
          "FROM users.user_by_comment " \
          "WHERE user_name = %s;"
    rows = cass_session.execute(cql, ls)
    functions = rows.all()
    return render_template('user/my_comments.html', args=functions, state="我的评论")


# 主页  模糊搜索
@user_bp.route('/search_function', methods=['POST'])
def search_functions():
    function_title = request.form.get('function_title_key')
    function_title_list = [function_title]
    function_title_cql = "SELECT * " \
                         "FROM functions.functions " \
                         "WHERE function_title " \
                         "LIKE %s " \
                         "LIMIT 9;"
    functions_rows = cass_session.execute(function_title_cql, function_title_list)
    functions = functions_rows.all()
    return render_template('index.html', functions=functions)


# 主页类型搜索
@user_bp.route('/search_type/<function_type>')
def search_type(function_type):
    function_type_list = [function_type]
    function_type_cql = "SELECT * " \
                        "FROM functions.functions " \
                        "WHERE function_type = %s;"
    functions_rows = cass_session.execute(function_type_cql, function_type_list)
    functions = functions_rows.all()
    return render_template('index.html', functions=functions, function_type=function_type)


# 主页时间搜素
@user_bp.route('/search_date', methods=['POST'])
def search_time():
    search_date = request.form.get('search_date')
    function_type_list = [search_date]
    function_type_cql = "SELECT * " \
                        "FROM functions.functions " \
                        "WHERE created_at_date = %s;"
    functions_rows = cass_session.execute(function_type_cql, function_type_list)
    functions = functions_rows.all()
    return render_template('index.html', functions=functions, search_date=search_date)


# 用户收藏某一个 Function
@user_bp.route('/collect/<function_id_str>')
@load_user
def collect_function(function_id_str):
    collection_by_user = session['user_name']
    # 查询出 FR 需要插入的信息
    function_id_uuid = uuid.UUID(function_id_str)

    # 判断用户是否已收藏 FR
    collection_query_list = [collection_by_user, function_id_uuid]
    collection_query_cql = "SELECT * " \
                           "FROM users.user_by_collection " \
                           "WHERE user_name = %s " \
                           "AND function_id = %s;"
    function_rows = cass_session.execute(collection_query_cql, collection_query_list)
    if len(function_rows.all()) != 0:
        flash("您已经收藏过该 项目")
        return redirect(url_for('index'))

    function_query_list = [function_id_uuid]
    function_query_cql = "SELECT function_type,function_title,created_at,state " \
                         "FROM functions.functions " \
                         "WHERE function_id = %s;"
    function_rows = cass_session.execute(function_query_cql, function_query_list)
    function_data = function_rows.all()
    function_type = function_data[0].get('function_type')
    function_title = function_data[0].get('function_title')
    created_at = function_data[0].get('created_at')
    state = function_data[0].get('state')

    # 更新表 functions.functions_collections_counter 的记录
    functions_collections_counter_list = [function_id_uuid, function_title]
    functions_collections_counter_cql = "UPDATE functions.functions_collections_counter " \
                                        "SET collections = collections +1 " \
                                        "WHERE function_id = %s AND function_title = %s;"
    cass_session.execute(functions_collections_counter_cql, functions_collections_counter_list)

    # 更新表 functions.functions_collections 的记录
    functions_collections_list = [function_id_uuid, collection_by_user, created_at, function_title, function_type]
    functions_collections_cql = "INSERT INTO functions.functions_collections (function_id, collection_by_user, " \
                                "created_at, function_title, function_type) " \
                                "VALUES (%s, %s, %s, %s, %s);"
    cass_session.execute(functions_collections_cql, functions_collections_list)

    # 更新表 users.user_by_collection 的记录
    user_by_collection_list = [collection_by_user, function_id_uuid, function_title, function_type, state]
    user_by_collection_cql = "INSERT INTO users.user_by_collection (user_name, function_id, function_title, " \
                             "function_type, state) " \
                             "VALUES (%s, %s, %s, %s, %s);"
    cass_session.execute(user_by_collection_cql, user_by_collection_list)
    flash("收藏成功")
    return redirect(url_for('user.my_collections'))


# 查看主页某一个已发布 FR 的详细信息
@user_bp.route('/functions_published/<function_id_str>')
def function_publisher(function_id_str):
    function_id_uuid = uuid.UUID(function_id_str)
    function_published_query_list = [function_id_uuid]
    function_published_query_cql = "SELECT * " \
                                   "FROM functions.functions " \
                                   "WHERE function_id = %s;"
    function_rows = cass_session.execute(function_published_query_cql, function_published_query_list)
    function_date = function_rows.all()
    return render_template('function_published_details.html', function=function_date)


# 用户编辑未审核的 FR
@user_bp.route('/edit_function_not_reviewed', methods=["POST"])
@load_user
def edit_function_not_reviewed():
    new_file_name = None
    if request.method == 'POST':
        file = request.files['function-cover']
        if not (file and allowed_file(file.filename)):
            flash("图片上传不符合规则")
            return render_template('user/create_new_function.html')
        base_path = os.path.dirname(__file__)  # 当前文件所在路径
        new_file_name = f"{cassandra.util.uuid_from_time(time.time())}.jpg"
        upload_path = os.path.join(base_path, '../../static/user_images', secure_filename(new_file_name))  # 重命名图片名
        file.save(upload_path)
    function_cover = '../../static/user_images' + new_file_name  # 封面路径
    function_id_str = request.form.get('function_id')
    function_id = uuid.UUID(function_id_str)  # id
    function_content = request.form.get('content')
    created_at = datetime.now()  # 创建时间
    function_type = request.form.get('type')  # 类型
    crowd_funding_days = int(request.form.get('days'))  # 众筹时间
    crowd_funding_money = int(request.form.get('money'))  # 众筹金额
    function_introduction = request.form.get('introduction')  # 简介
    function_title = request.form.get('title')  # 标题
    publisher = session.get('user_name')
    state = "未审核"
    comments = None
    # 更新 FR 到 functions.functions_request
    function_request_list = [comments, created_at, crowd_funding_days, crowd_funding_money,
                             function_content, function_cover, function_introduction, function_title, function_type,
                             publisher, state, function_id]
    function_request_cql = "UPDATE functions.functions_request " \
                           "SET comments = %s, created_at = %s, crowd_funding_days = %s, " \
                           "crowd_funding_money = %s,  function_content = %s, function_cover = %s, " \
                           "function_introduction = %s, function_title = %s , function_type = %s, " \
                           " publisher = %s,  state  = %s " \
                           "WHERE function_id = %s;"
    cass_session.execute(function_request_cql, function_request_list)

    # 添加 FR 到 functions_request_by_status
    function_request_by_status_list = [created_at, function_title, function_type, publisher, state, function_id]
    function_request_by_status_cql = "UPDATE functions.functions_request_by_status " \
                                     "SET created_at = %s, function_title = %s, function_type = %s, publisher = %s " \
                                     "WHERE state = %s " \
                                     "AND function_id = %s;"
    cass_session.execute(function_request_by_status_cql, function_request_by_status_list)

    # 添加任务到 users.user_by_publish, 先删再插入
    user_by_publish_delete_list = [publisher, function_id]
    user_by_publish_delete_cql = "DELETE " \
                                 "FROM users.user_by_publish " \
                                 "WHERE user_name = %s " \
                                 "AND function_id = %s;"
    cass_session.execute(user_by_publish_delete_cql, user_by_publish_delete_list)
    # 插入
    user_by_publish_list = [publisher, function_id, created_at, function_title, function_type, state]
    user_by_publish_cql = "INSERT INTO users.user_by_publish " \
                          "(user_name, function_id, create_at, function_title, function_type, state) " \
                          "VALUES (%s,%s,%s,%s,%s,%s);"
    cass_session.execute(user_by_publish_cql, user_by_publish_list)

    flash("任务更新成功！")
    return redirect(url_for('user.user_functions', state=state))


#  用户删除自己未审核的任务
@user_bp.route('/delete_function_not_reviewed', methods=['POST'])
@load_user
def delete_function_not_reviewed():
    function_id = uuid.UUID(request.form.get('function_id'))
    state = request.form.get('state')
    user_name = session.get('user_name')

    # 删除 functions.functions_request 表里的记录
    functions_request_delete_list = [function_id]
    functions_request_delete_cql = "DELETE " \
                                   "FROM functions.functions_request " \
                                   "WHERE function_id = %s;"
    cass_session.execute(functions_request_delete_cql, functions_request_delete_list)

    # 删除 functions.functions_request_by_status 表的记录
    functions_request_by_status_delete_list = [state, function_id]
    functions_request_by_status_delete_cql = "DELETE " \
                                             "FROM functions.functions_request_by_status " \
                                             "WHERE state = %s " \
                                             "AND function_id = %s;"
    cass_session.execute(functions_request_by_status_delete_cql, functions_request_by_status_delete_list)

    # 删除 users.user_by_publish 表的记录
    user_by_publish_delete_list = [user_name, function_id]
    user_by_publish_delete_cql = "DELETE " \
                                 "FROM users.user_by_publish " \
                                 "WHERE user_name = %s " \
                                 "AND function_id = %s;"
    cass_session.execute(user_by_publish_delete_cql, user_by_publish_delete_list)
    flash("删除成功")
    return redirect(url_for('user.user_functions', state=state))


# 用户打赏跳转
@user_bp.route('/donating', methods=['POST'])
@load_user
def donating():
    function_id = request.form.get('function_id')
    publisher = request.form.get('publisher')
    user_name = session['user_name']
    if publisher == user_name:
        flash("不能给自己打赏")
        return redirect(url_for('index'))
    return render_template('user/user_donate_function.html', function_id=function_id)


# 用户打赏一个 FR
@user_bp.route('/upload_donation', methods=["POST"])
@load_user
def donate_function():
    # 先查询账户余额是否能够打赏
    user_account = request.form.get('user_account')
    function_id_uuid = uuid.UUID(request.form.get('function_id'))
    donate_money = int(request.form.get('money'))
    if donate_money > int(user_account):
        flash("账户余额不足")
        return redirect(url_for('index'))
    # 查询当前已筹集的金额
    donate_money_query_list = [function_id_uuid]
    donate_money_query_cql = "SELECT * " \
                             "FROM functions.functions " \
                             "WHERE function_id = %s;"
    donated_function_rows = cass_session.execute(donate_money_query_cql, donate_money_query_list)
    donated_function = donated_function_rows.all()[0]
    current_donate_money = donated_function.get('crowd_funding_current_money')
    # 更新 functions.functions 表里的已筹集金额
    crowd_funding_current_money = current_donate_money + donate_money
    donate_function_update_list = [crowd_funding_current_money, function_id_uuid]
    donate_function_update_cql = "UPDATE functions.functions " \
                                 "SET crowd_funding_current_money = %s " \
                                 "WHERE function_id = %s;"
    cass_session.execute(donate_function_update_cql, donate_function_update_list)

    # 插入数据到 users.user_by_contribution 表
    created_at = datetime.now()
    user_by_contribution_insert_list = [session['user_name'], function_id_uuid, created_at,
                                        donated_function.get('function_title'),
                                        donated_function.get('function_type'), donate_money,
                                        donated_function.get('state')]
    user_by_contribution_insert_cql = "INSERT INTO users.user_by_contribution " \
                                      "(user_name, function_id, create_at, function_title, function_type, money, " \
                                      "state) " \
                                      "VALUES (%s, %s, %s, %s, %s, %s, %s);"
    cass_session.execute(user_by_contribution_insert_cql, user_by_contribution_insert_list)

    # 插入到 functions.functions_contribution 表
    functions_contribution_insert_list = [function_id_uuid, created_at, session['user_name'], donate_money]
    functions_contribution_insert_cql = "INSERT INTO functions.functions_contribution " \
                                        "(function_id, created_at, contribution_by_user, money) " \
                                        "VALUES (%s, %s, %s, %s);"
    cass_session.execute(functions_contribution_insert_cql, functions_contribution_insert_list)

    # 用户账户减去相应金额
    user_name = session['user_name']
    user_money_query_list = [user_name]
    user_money_query_cql = "SELECT user_account " \
                           "FROM users.user " \
                           "WHERE user_name = %s;"
    user_money_rows = cass_session.execute(user_money_query_cql, user_money_query_list)
    user_money = user_money_rows.all()[0].get('user_account')
    current_user_account = user_money - donate_money
    user_money_insert_list = [current_user_account, user_name]
    user_money_insert_cql = "UPDATE users.user " \
                            "SET user_account = %s " \
                            "WHERE user_name = %s;"
    cass_session.execute(user_money_insert_cql, user_money_insert_list)
    flash("打赏成功")
    return redirect(url_for('index'))
