import time
from flask import Blueprint, request, jsonify

from util.post_response import get_return_response

# mongodb数据库连接
from connect_db.connect_mongo import ConnectMongoDB, ObjectId
# from ueditor import UEditor
from util.post_response import get_return_response

comment = Blueprint("comment", __name__)

# app = Flask(__name__)
# ue = UEditor(app)

connection = ConnectMongoDB()  # 连接数据库
comment_collection = connection.get_collection('comment')  # 评论表
blog_collection = connection.get_collection('blog')  # 博客表


@comment.route('/get_blog_comments', methods=['Post', ])
def get_blog_comments():
    """
    获取博客评论
    :return:
    """
    form = request.form
    print(form)
    blog_id = form.get('blog_id')
    results = connection.find_data(comment_collection, {'$and': [{'blog_id': ObjectId(blog_id)}, {'is_del': 0}]})
    comments = []
    for result in results:
        comment_temp = {}
        comment_temp['username'] = result['username']
        comment_temp['create_time'] = result['create_time']
        comment_temp['content'] = result['content']
        comments.append(comment_temp)
    print({"status": True, "data": comments})
    response = get_return_response(
        jsonify({"status": True, "data": comments}))
    return response


@comment.route('/comment_add', methods=['Post', ])
def comment_add():
    """
    添加博客
    :return:
    """
    form = request.form
    print(form)
    info = {}
    info['user_id'] = ObjectId(form.get('user_id'))
    info['username'] = form.get('username')
    info['blog_id'] = ObjectId(form.get('blog_id'))

    blog_temp = connection.find_one_data(blog_collection, info['blog_id'])
    info['blog_name'] = blog_temp['title']
    info['content'] = form.get('content')
    info['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    info['response'] = {}
    info['is_del'] = 0
    comment_id = connection.insert_list(comment_collection, info)
    print({"status": True, "data": {'comment_id': str(comment_id)}})
    response = get_return_response(jsonify({"status": True, "data": {'comment_id': str(comment_id)}}))
    return response
