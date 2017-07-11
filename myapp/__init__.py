from flask import Flask

from userinfo.userinfo import userinfo
from blog.blog import blog

# [...] Initialize the app

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config.default')
app.config.from_pyfile('config.py')  # 从instance文件夹中加载配置


# app.config.from_envvar(‘APP_CONFIG_FILE’)将加载由环境变量APP_CONFIG_FILE指定的文件。这个环境变量的值应该是一个配置文件的绝对路径。
# APP_CONFIG_FILE=/var/www/yourapp/config/production.py
# python llws_blog_manage.py
# app.config.from_envvar('APP_CONFIG_FILE')


def run():
    app.register_blueprint(userinfo, url_prefix='/userinfo')
    app.register_blueprint(blog, url_prefix='/blog')
    app.run(host='0.0.0.0', debug=app.config['DEBUG'],port=8188)

if __name__ == '__main__':
    run()
    # app.run(host='0.0.0.0', debug=True)
