#默认值，适用于所有的环境或交由具体环境进行覆盖。举个例子，在config/default.py中设置DEBUG = False，在config/development.py中设置DEBUG = True。
DEBUG = False # 启动Flask的Debug模式
SQLALCHEMY_ECHO = False
BCRYPT_LEVEL = 13 # 配置Flask-Bcrypt拓展
MAIL_FROM_EMAIL = "robert@example.com" # 设置邮件来源