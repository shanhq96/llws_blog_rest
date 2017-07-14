from flask import Blueprint, request, jsonify
from pymongo import DESCENDING

from util.post_response import get_return_response

# mongodb数据库连接
from connect_db.connect_mongo import ConnectMongoDB, ObjectId
# from ueditor import UEditor
from util.post_response import get_return_response

blog = Blueprint("blog", __name__)

# app = Flask(__name__)
# ue = UEditor(app)

connection = ConnectMongoDB()  # 连接数据库
blog_collection = connection.get_collection('blog')  # 博客表
blog_userinfo_collection = connection.get_collection('blog_userinfo')  # 博客用户表


@blog.route('/get_blog_list', methods=['Post', ])
def get_blog_list():
    """
    获取博客列表
    :return:
    """
    form = request.form
    print(form)
    want_page = int(form.get('want_page'))  # 当前页数
    want_data_per_page = int(form.get('want_data_per_page'))  # 要求的一页的数据
    is_top = form.get('is_top') == 'true'  # 是否置顶的文章

    pos = want_page * want_data_per_page

    # 查询数据库
    result_temp = connection.find_data(blog_collection, {'$and': [{"is_top": is_top}, {'is_status': 1}]})
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
        response_data['title_img_url'] = result_data['title_img_url']
        response_data_array.append(response_data)
    print({"status": True,
           "data": {"want_page": want_page, "total_blog_num": total_blog_num, "blog_list": response_data_array}})
    response = get_return_response(
        jsonify({"status": True,
                 "data": {"want_page": want_page, "total_blog_num": total_blog_num, "blog_list": response_data_array}}))
    return response


@blog.route('/get_one_blog', methods=['Post', ])
def get_one_blog():
    """
        获取博客详情
        :return:
        """
    form = request.form
    print(form)
    blog_id = form.get('blog_id')  # 要查看的博客id
    user_id = form.get('user_id')  # 请求的用户id
    if(user_id != "null"):
        blog_userinfo = connection.find_one_data(blog_userinfo_collection, user_id)
        the_interests = blog_userinfo['interests']
    else:
        the_interests = []

    # 查询数据库
    result = connection.find_one_data(blog_collection, blog_id)

    # 构造返回的data
    response_data = {}
    response_data['_id'] = str(result['_id'])
    response_data['title'] = result['title']
    response_data['update_time'] = result['update_time']
    response_data['content'] = result['content']
    response_data['big_label_name'] = result['big_label_name']
    response_data['small_label_name'] = result['small_label_name']
    response_data['is_collect'] = ObjectId(blog_id) in the_interests
    print({"status": True, "data": response_data})
    response = get_return_response(
        jsonify({"status": True, "data": response_data}))
    update_blog_hits(blog_id)   # 更新访问量
    return response


def update_blog_hits(blog_id):
    """
    更新博客点击量
    :param blog_id:
    :return:
    """
    result = connection.find_one_data(blog_collection, blog_id)
    the_hits = result['hits'] + 1
    connection.update_data(blog_collection,{'_id':ObjectId(blog_id)}, {'$set': {'hits': the_hits}})
    return True