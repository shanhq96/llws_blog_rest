from flask import make_response


def get_return_response(data2return):
    # 获取封装着返回数据的response
    response = make_response(data2return)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response