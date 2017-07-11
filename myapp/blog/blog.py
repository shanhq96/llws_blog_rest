from flask import Blueprint, request, jsonify

from util.post_response import get_return_response

blog = Blueprint("blog", __name__)


@blog.route('/get_blog_list', methods=['Post', ])
def get_blog_list():
    """
    获取博客列表
    :return:
    """
    test_totle_data_num = 5

    temp = request
    form = request.form
    want_page = int(form.get('want_page'))  # 当前页数
    want_data_per_page = int(form.get('want_data_per_page')) # 要求的一页的数据
    total_blog_num = test_totle_data_num

    response_data_array = []
    for i in range(want_data_per_page):
        j = i + 1
        response_data = {}
        response_data['id'] = j
        response_data['title'] = '第%s篇测试文章的标题' % (j)
        response_data['describe'] = '第%s篇测试文章的描述' % (j)
        # response_data['big_label'] = 1
        # response_data['small_label'] = 1
        response_data['url'] = '第%s篇测试文章的url' % (j)
        response_data['title_img_url'] = "/static/title_imgs/20ev2.jpg"
        # response_data['create_time'] = 1
        # response_data['update_time'] = 1
        # response_data['hits'] = 1
        response_data['is_top'] = j <= 3
        # response_data['is_status'] = 1
        response_data_array.append(response_data)

    # TODO 查询数据库中的用户名密码是否一致
    response = get_return_response(
        jsonify({"status": True,
                 "data": {"want_page": want_page, "total_blog_num": total_blog_num, "blog_list": response_data_array}}))
    return response

    # @userinfo.route('/sign_in_get/<username>',methods=['Get',])
    # def sign_in_get(username):
    #     print(username)
