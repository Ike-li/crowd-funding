from flask import Flask, render_template
from flask_ckeditor import CKEditor

from src.apps.club.admin.views import admin_bp
from src.apps.club.user.views import user_bp
from src.apps.settings import DevelopmentConfig

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
        return render_template('index.html')


    return app
