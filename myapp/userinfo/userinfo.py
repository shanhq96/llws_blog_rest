from flask import Blueprint, request, jsonify

from util.post_response import get_return_response

userinfo = Blueprint("userinfo", __name__)


@userinfo.route('/sign_in',methods=['Post',])
def sign_in():
    """
    验证用户名和密码是否正确
    :return:
    """
    temp = request
    form = request.form
    print(form)
    username = form.get('username')
    passwd = form.get('passwd')
    print('用户名：%s，密码：%s'%(username,passwd))
    flag = username == "admin" and passwd == "123456"
    # TODO 查询数据库中的用户名密码是否一致
    response = get_return_response(
        jsonify({"status": flag, "data": {"username": username}}))
    return response

# @userinfo.route('/sign_in_get/<username>',methods=['Get',])
# def sign_in_get(username):
#     print(username)