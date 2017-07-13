from flask import Blueprint, request, jsonify

from util.post_response import get_return_response
from urllib import request as urllib_request,parse
import http.cookiejar

weather = Blueprint("weather", __name__)


@weather.route('/get_weather',methods=['Post',])
def get_weather():
    """
    获取天气
    :return:
    """
    form = request.form
    city_name = form.get('city_name')
    response_data = get_new_weather(city_name)
    response = get_return_response(
        jsonify({"status": True,"data": response_data}))
    return response



def get_opener():
    cj = http.cookiejar.CookieJar()
    opener = urllib_request.build_opener(urllib_request.HTTPCookieProcessor(cj))
    return opener

def get_new_weather(city_name="哈尔滨"):
    api_key = 'b24c306dfb27448e820c6046a34cda94'
    url = 'http://apis.haoservice.com/weather?cityname=' + city_name + '&key=' + api_key
    print(parse.quote(url, safe='/:?=&'))
    opener = get_opener()
    uop = opener.open(parse.quote(url, safe='/:?=&'), timeout=1000)
    data = uop.read().decode()
    # data = '''{"error_code":0,"reason":"成功","result":{"sk":{"temp":"30","wind_direction":"西南风","wind_strength":"4级","humidity":"46","time":"16:46"},"today":{"city":"哈尔滨","date_y":"2017年07月12日","week":"星期三","temperature":"24~32","weather":"多云","fa":"01","fb":"01","wind":"西风 3-4 级","dressing_index":"炎热","dressing_advice":"天气炎热，建议着短衫、短裙、短裤、薄型T恤衫等清凉夏季服装。","uv_index":"中等","comfort_index":"--","wash_index":"较适宜","travel_index":"较适宜","exercise_index":"较适宜","drying_index":"--"},"future":[{"temperature":"20~29","weather":"多云","fa":"01","fb":"04","wind":"西风 3-4 级","week":"星期四","date":"20170713"},{"temperature":"21~32","weather":"多云","fa":"01","fb":"01","wind":"西南风 3-4 级","week":"星期五","date":"20170714"},{"temperature":"20~29","weather":"多云","fa":"01","fb":"01","wind":"西北风 微风","week":"星期六","date":"20170715"},{"temperature":"20~30","weather":"多云","fa":"01","fb":"04","wind":"西南风 微风","week":"星期日","date":"20170716"},{"temperature":"21~32","weather":"雷阵雨","fa":"04","fb":"04","wind":"西南风 微风","week":"星期一","date":"20170717"},{"temperature":"21~31","weather":"雷阵雨","fa":"04","fb":"04","wind":"西南风 微风","week":"星期二","date":"20170718"},{"temperature":"19~29","weather":"多云","fa":"01","fb":"04","wind":"西南风 微风","week":"星期三","date":"20170719"},{"temperature":"18~27","weather":"雷阵雨","fa":"04","fb":"03","wind":" 微风","week":"星期四","date":"20170720"},{"temperature":"17~28","weather":"晴","fa":"00","fb":"00","wind":"西北风 微风","week":"星期五","date":"20170721"}]}}'''
    b = eval(data)
    print(data)
    response_data = {}
    if(b['error_code']==0):
        result = b['result']
        today_weather = result['today']
        response_data['min_temperature'] = today_weather['temperature'].split('~')[0]
        response_data['max_temperature'] = today_weather['temperature'].split('~')[1]
        response_data['date_y'] = today_weather['date_y']
        response_data['weather'] = today_weather['weather']
        response_data['city_name'] = city_name
        print(response_data)
    return response_data


if(__name__=="__main__"):
    get_new_weather()