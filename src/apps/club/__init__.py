import uuid
from datetime import datetime

from flask import Flask, render_template, request
from flask_ckeditor import CKEditor

from src.apps.club.admin.views import admin_bp
from src.apps.club.user.views import user_bp
from src.apps.settings import DevelopmentConfig, cass_session

ckeditor = CKEditor()


def create_app():
    # 创建 flask 对象 app, templates 目录 为 club/init.py 的 上一级目录，需要加 template_folder, 同理 static。
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # 使用 settings.py 配置文件。
    app.config.from_object(DevelopmentConfig)

    # 注册蓝图，url_prefix 为各个小模块创建路由前缀。
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_perfix='/user')

    # 实例化CKEditor类
    ckeditor.init_app(app)

    # 退款函数
    def refund(function_id):
        refund_functions_query_list = [function_id]
        refund_functions_query_cql = "SELECT contribution_by_user, money " \
                                     "FROM functions.functions_contribution " \
                                     "WHERE function_id = %s;"
        money_list_rows = cass_session.execute(refund_functions_query_cql, refund_functions_query_list)
        money_list = money_list_rows.all()
        for money_dict in money_list:
            user_name = money_dict.get('contribution_by_user')
            money = money_dict.get('money')
            user_account_query_list = [user_name]
            user_account_query_cql = "SELECT user_account " \
                                     "FROM users.user " \
                                     "WHERE user_name = %s;"
            user_account_by_query = (cass_session.execute(user_account_query_cql, user_account_query_list)).all()
            user_account_insert_list = [user_name, user_account_by_query[0].get('user_account') + money]
            user_account_insert_cql = "INSERT INTO users.user" \
                                      "(user_name,user_account) " \
                                      "VALUES (%s, %s);"
            cass_session.execute(user_account_insert_cql, user_account_insert_list)
            return None

    # 首页
    @app.route('/', methods=["GET", "POST"])
    def index():
        function_id = request.form.get('function_id')
        if function_id is None:
            functions_cql = "SELECT * " \
                            "FROM functions.functions " \
                            "limit 9;"
            functions_rows = cass_session.execute(functions_cql)
            functions = functions_rows.all()
            for function in functions:
                if function.get('closing_time') < (datetime.now()):
                    if function.get('crowd_funding_current_money') >= function.get('crowd_funding_money'):
                        # 插入到 functions.success_functions 表
                        success_function_insert_list = [function.get('function_id'), function.get('closing_time'),
                                                        function.get('created_at'), function.get('created_at_date'),
                                                        function.get('crowd_funding_days'),
                                                        function.get('crowd_funding_money'),
                                                        function.get('function_content'),
                                                        function.get('function_cover'),
                                                        function.get('function_introduction'),
                                                        function.get('function_title'),
                                                        function.get('function_type'), function.get('publisher')]
                        success_function_insert_cql = "INSERT INTO functions.success_functions " \
                                                      "(function_id, closing_time, created_at, created_at_date, " \
                                                      "crowd_funding_days, crowd_funding_money, function_content, " \
                                                      "function_cover, function_introduction, function_title, " \
                                                      "function_type, publisher) " \
                                                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        cass_session.execute(success_function_insert_cql, success_function_insert_list)
                        # 删除 functions.functions 表里的 记录
                        delete_function_list = [function.get('function_id')]
                        delete_function_cql = "DELETE FROM " \
                                              "functions.functions " \
                                              "WHERE function_id = %s;"
                        cass_session.execute(delete_function_cql, delete_function_list)
                    else:
                        # 插入到 functions.fail_functions 表
                        fail_function_insert_list = [function.get('function_id'), function.get('closing_time'),
                                                     function.get('created_at'), function.get('created_at_date'),
                                                     function.get('crowd_funding_days'),
                                                     function.get('crowd_funding_money'),
                                                     function.get('function_content'), function.get('function_cover'),
                                                     function.get('function_introduction'),
                                                     function.get('function_title'),
                                                     function.get('function_type'), function.get('publisher')]
                        fail_function_insert_cql = "INSERT INTO functions.fail_functions " \
                                                   "(function_id, closing_time, created_at, created_at_date, " \
                                                   "crowd_funding_days, crowd_funding_money, function_content, " \
                                                   "function_cover, function_introduction, function_title, " \
                                                   "function_type, publisher) " \
                                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        cass_session.execute(fail_function_insert_cql, fail_function_insert_list)
                        # 删除 fail_functions 表里的 记录
                        delete_function_list = [function.get('function_id')]
                        delete_function_cql = "DELETE FROM " \
                                              "functions.functions " \
                                              "WHERE function_id = %s;"
                        cass_session.execute(delete_function_cql, delete_function_list)
                        # 退款
                        refund(function.get('function_id'))
                        # 删除 functions.functions_contribution 里的记录
                        delete_functions_contribution_list = [function.get('function_id')]
                        delete_functions_contribution_cql = "DELETE FROM functions.functions_contribution " \
                                                            "WHERE function_id = %s;"
                        cass_session.execute(delete_functions_contribution_cql, delete_functions_contribution_list)

            return render_template('index.html', functions=functions)
        else:
            functions_page_list = [uuid.UUID(function_id)]
            functions_page_cql = "SELECT * " \
                                 "FROM functions.functions " \
                                 "WHERE token(function_id) > token(%s) " \
                                 "limit 9;"
            functions_page_rows = cass_session.execute(functions_page_cql, functions_page_list)
            functions_page = functions_page_rows.all()
            for function in functions_page:
                if function.get('closing_time') < (datetime.now()):
                    if function.get('crowd_funding_current_money') >= function.get('crowd_funding_money'):
                        # 插入到 functions.success_functions 表
                        success_function_insert_list = [function.get('function_id'), function.get('closing_time'),
                                                        function.get('created_at'), function.get('created_at_date'),
                                                        function.get('crowd_funding_days'),
                                                        function.get('crowd_funding_money'),
                                                        function.get('function_content'),
                                                        function.get('function_cover'),
                                                        function.get('function_introduction'),
                                                        function.get('function_title'),
                                                        function.get('function_type'), function.get('publisher')]
                        success_function_insert_cql = "INSERT INTO functions.success_functions " \
                                                      "(function_id, closing_time, created_at, created_at_date, " \
                                                      "crowd_funding_days, crowd_funding_money, function_content, " \
                                                      "function_cover, function_introduction, function_title, " \
                                                      "function_type, publisher) " \
                                                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        cass_session.execute(success_function_insert_cql, success_function_insert_list)
                        # 删除 functions.functions 表里的 记录
                        delete_function_list = [function.get('function_id')]
                        delete_function_cql = "DELETE FROM " \
                                              "functions.functions WHERE function_id = %s;"
                        cass_session.execute(delete_function_cql, delete_function_list)
                    else:
                        # 插入到 functions.fail_functions 表
                        fail_function_insert_list = [function.get('function_id'), function.get('closing_time'),
                                                     function.get('created_at'), function.get('created_at_date'),
                                                     function.get('crowd_funding_days'),
                                                     function.get('crowd_funding_money'),
                                                     function.get('function_content'), function.get('function_cover'),
                                                     function.get('function_introduction'),
                                                     function.get('function_title'),
                                                     function.get('function_type'), function.get('publisher')]
                        fail_function_insert_cql = "INSERT INTO functions.fail_functions " \
                                                   "(function_id, closing_time, created_at, created_at_date, " \
                                                   "crowd_funding_days, crowd_funding_money, function_content, " \
                                                   "function_cover, function_introduction, function_title, " \
                                                   "function_type, publisher) " \
                                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        cass_session.execute(fail_function_insert_cql, fail_function_insert_list)
                        # 删除 functions.functions 表里的 记录
                        delete_function_list = [function.get('function_id')]
                        delete_function_cql = "DELETE FROM " \
                                              "functions.functions WHERE function_id = %s;"
                        cass_session.execute(delete_function_cql, delete_function_list)
                        # 退款
                        refund(function.get('function_id'))
                        # 删除 functions.functions_contribution 里的记录
                        delete_functions_contribution_list = [function.get('function_id')]
                        delete_functions_contribution_cql = "DELETE FROM functions.functions_contribution " \
                                                            "WHERE function_id = %s;"
                        cass_session.execute(delete_functions_contribution_cql, delete_functions_contribution_list)
            return render_template('index.html', functions=functions_page)

    # 404 error handler
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.route('/base')
    def base():
        return render_template('base.html')

    @app.route('/user_base')
    def user_base():
        return render_template('user/user_base.html')

    @app.route('/test', methods=["GET", "POST"])
    def index1():
        function_id = request.form.get('function_id')
        print(function_id)
        return 'ok'

    return app
