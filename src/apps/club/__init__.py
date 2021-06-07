from datetime import datetime

from flask import Flask, render_template
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

    # 首页
    @app.route('/')
    def index():
        functions_cql = "SELECT * " \
                        "FROM functions.functions;"
        functions_rows = cass_session.execute(functions_cql)
        functions = functions_rows.all()
        for function in functions:
            if function.get('closing_time') < (datetime.now()):
                print("到期")
                if function.get('crowd_funding_current_money') >= function.get('crowd_funding_money'):
                    print("众筹成功")
                    # 插入到 functions.success_functions 表
                    success_function_insert_list = [function.get('function_id'), function.get('closing_time'),
                                                    function.get('created_at'), function.get('created_at_date'),
                                                    function.get('crowd_funding_days'),
                                                    function.get('crowd_funding_money'),
                                                    function.get('function_content'), function.get('function_cover'),
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
                    print("插入 success_function")
                    # 删除 functions.functions 表里的 记录
                    delete_function_list = [function.get('function_id')]
                    delete_function_cql = "DELETE FROM " \
                                          "functions.functions WHERE function_id = %s;"
                    cass_session.execute(delete_function_cql, delete_function_list)
                else:
                    print("众筹失败")
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
                    print("插入 fail_function")
                    # 删除 functions.functions 表里的 记录
                    delete_function_list = [function.get('function_id')]
                    delete_function_cql = "DELETE FROM " \
                                          "functions.functions WHERE function_id = %s;"
                    cass_session.execute(delete_function_cql, delete_function_list)
            else:
                print("没到期")
        # current_time = datetime.now()
        # closing_time = functions[0].get('closing_time')
        # function_id =
        # print(functions[0])
        # if current_time == closing_time:
        #     return redirect(url_for('user'))
        return render_template('index.html', functions=functions)

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

    return app
