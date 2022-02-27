from flask_script import Manager

from src.apps.club import create_app

app = create_app()

manager = Manager(
    app=app
)  # 命令工具，使用 flask-script 脚本执行命令 python app.py runserver -h 0.0.0.0[ip] -p 5000[端口号]。

if __name__ == "__main__":
    manager.run()
