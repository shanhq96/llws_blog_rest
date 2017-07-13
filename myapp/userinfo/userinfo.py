import time
from flask import Blueprint, request, jsonify
from pymongo import DESCENDING

from connect_db.connect_mongo import ConnectMongoDB, ObjectId
from util.post_response import get_return_response

userinfo = Blueprint("userinfo", __name__)

connection = ConnectMongoDB()  # 连接数据库
blog_userinfo_collection = connection.get_collection('blog_userinfo_collection')  # 博客用户表
blog_collection = connection.get_collection('blog')  # 博客表


@userinfo.route('/sign_in', methods=['Post', ])
def sign_in():
    """
    验证用户名和密码是否正确
    :return:
    """
    form = request.form
    print(form)
    username = form.get('username')
    passwd = form.get('passwd')
    print('用户名：%s，密码：%s' % (username, passwd))
    results = connection.find_data(blog_userinfo_collection, {"username": username, "passwd": passwd, "is_status": 1})
    if (results.count() == 1):
        for result in results:
            connection.update_data(blog_userinfo_collection, {'username': username}, {'$set': {
                'last_login_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}})
            response_data = {"status": True, "data": {"username": username, "user_id": str(result['_id'])}}

    else:
        response_data = {"status": False, "data": {}}
    print(response_data)
    response = get_return_response(jsonify(response_data))
    return response


@userinfo.route('/register', methods=['Post', ])
def register():
    """
    注册新用户
    :return:
    """
    form = request.form
    info = {}
    info['username'] = form.get('username')
    info['passwd'] = form.get('passwd')
    info['is_status'] = 1
    info['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    info['last_login_time'] = ''
    info['last_login_ip'] = ''
    info['interests'] = []  # 兴趣列表为空
    user_id = connection.insert_list(blog_userinfo_collection, info)
    response = get_return_response(
        jsonify({"status": True, "data": {"username": info['username'], "user_id": str(user_id)}}))
    return response


@userinfo.route('/valid_username', methods=['Post', ])
def valid_username():
    """
    验证用户名是否重复
    :return:
    """
    form = request.form
    print(form)
    username = form.get('username')
    results = connection.find_data(blog_userinfo_collection, {'username': username})
    flag = results.count() == 0
    print({"status": flag, "data": {}})
    response = get_return_response(
        jsonify({"status": flag, "data": {}}))
    return response


@userinfo.route('/blog_collect', methods=['Post', ])
def blog_collect():
    """
    收藏博客文章
    :return:
    """
    form = request.form
    print(form)
    _id = ObjectId(form.get('_id'))
    user_id = form.get('user_id')
    blog_userinfo_temp = connection.find_one_data(blog_userinfo_collection, user_id)

    the_interests = blog_userinfo_temp['interests']
    if (_id not in the_interests):
        the_interests.append(_id)
    connection.update_data(blog_userinfo_collection, {'_id': ObjectId(user_id)}, {"$set": {"interests": the_interests}})
    response = get_return_response(
        jsonify({"status": True, "data": {}}))
    return response


@userinfo.route('/cancel_blog_collect', methods=['Post', ])
def cancel_blog_collect():
    """
    取消收藏博客文章
    :return:
    """
    form = request.form
    _id = ObjectId(form.get('_id'))
    user_id = form.get('user_id')
    blog_userinfo_temp = connection.find_one_data(blog_userinfo_collection, user_id)

    the_interests = blog_userinfo_temp['interests']
    if (_id in the_interests):
        the_interests.remove(_id)
    connection.update_data(blog_userinfo_collection, {'_id': ObjectId(user_id)}, {"$set": {"interests": the_interests}})
    response = get_return_response(
        jsonify({"status": True, "data": {}}))
    return response


@userinfo.route('/get_all_collected_blog',methods=['Post',])
def get_all_collected_blog():
    form = request.form
    print(form)
    user_id = form.get('user_id')
    userinfo_temp = connection.find_one_data(blog_userinfo_collection,user_id)
    the_interests = userinfo_temp['interests']  # 用户喜欢的房源列表

    print(form)
    want_page = int(form.get('want_page'))  # 当前页数
    want_data_per_page = int(form.get('want_data_per_page'))  # 要求的一页的数据

    pos = want_page * want_data_per_page

    # 查询数据库
    result_temp = connection.find_data(blog_collection, {'$and':[{"_id":{"$in":the_interests}},{'is_status':1}]})
    result = result_temp.skip(pos).limit(want_data_per_page).sort([('update_time',DESCENDING)])
    total_blog_num = result_temp.count()  # 博客总数

    # 构造返回的data
    response_data_array = []
    for result_data in result:
        response_data = {}
        response_data['_id'] = str(result_data['_id'])
        response_data['title'] = result_data['title']
        response_data['describe'] = result_data['describe']
        # response_data['title_img_url'] = result_data['title_img_url']
        response_data['title_img_url'] = '/static/title_imgs/20ev2.jpg'
        response_data_array.append(response_data)
    print({"status": True,
           "data": {"want_page": want_page, "total_blog_num": total_blog_num, "blog_list": response_data_array}})
    response = get_return_response(
        jsonify({"status": True,
                 "data": {"want_page": want_page, "total_blog_num": total_blog_num, "blog_list": response_data_array}}))
    return response