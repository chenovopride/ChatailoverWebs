import sys
# 将父目录添加到系统路径
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from datetime import datetime
# from route.route import databases
from collections import OrderedDict
from wrapper import *
from mongo_client_init import *

app = Flask(__name__)

selected_version = None
output_data = None
selected_query_type = None

# cat_mapping = {


# }

@app.route('/')
def index():
    return render_template('index.html', selected_version=selected_version, output_data=output_data, selected_query_type=selected_query_type)

@app.route('/query', methods=['POST'])
def query_balance():
    global selected_version, output_data, selected_query_type
    version = request.form.get('version')
    qq_id = request.form.get('data')
    query_type = request.form.get('query_type')
    # query_type = request.form.get('query_type','purchase')
    
    if not qq_id.isdigit():
        return jsonify({'error': '请输入有效的qq号'})

    if selected_version is None:
        return jsonify({'error': '请先选择bot购买的版本'})
    
    if query_type is None:
        print('查询类型：',query_type)
        return jsonify({'error': '请选择查询类型'})
    
    if version == '查理苏':
        # db = databases['db55']
        database = client[db_name_to_db['55']]
    elif version == '陆沉':
        # db = databases['db66']
        database = client[db_name_to_db['66']]
    elif version == '夏鸣星':
        # db = databases['db00']
        database = client[db_name_to_db['00']]
    elif version == '齐司礼':
        # db = databases['db77']
        database = client[db_name_to_db['77']]
    elif version == '萧逸':
        # db = databases['db11']
        database = client[db_name_to_db['11']]
    elif version == '沈星回':
        # db = databases['dbSXH']
        database = client[db_name_to_db['sxh']]
    elif version == '黎深':
        # db = databases['dbLS']
        database = client[db_name_to_db['ls']]
    elif version == '祁煜':
        # db = databases['dbQY']
        database = client[db_name_to_db['qy']]
    elif version == '夏以昼':
        # db = databases['dbXYZ']
        database = client[db_name_to_db['xyz']]
    elif version == '秦彻':
        # db = databases['dbQC']
        database = client[db_name_to_db['qc']]
    else:
        return jsonify({'error': '未上线的版本'})


    user_limit_collection = database['user_limit']

    # 服务器注释 
    # print(f'Debug: user_limit_collection = {user_limit_collection}')
    # print(f'Debug: user_info_collection = {user_info_collection}')
    
    if user_limit_collection is None:
        return jsonify({'error': '集合不存在，请确认数据库配置'})
    
    # 查询user_limit表和查询内容
    user_limit = user_limit_collection.find_one({"id": qq_id})
    if not user_limit:
        return jsonify({'error': f'找不到qq用户{qq_id}的购买信息，请联系管理员确认购买情况'})
    result = {}

    date_value = user_limit.get("date", str(datetime.date.today()))
    count_value = user_limit.get("count", 0)
    rate_value = user_limit.get("rate", 0)
    yueka_days = user_limit.get("days", 0)
        
    # 获取当前日期
    current_date = str(datetime.date.today())
    date_format = "%Y-%m-%d"
    date_now = datetime.datetime.strptime(current_date, date_format).date()
    date_bought = datetime.datetime.strptime(date_value, date_format).date() if date_value else date_now
    days_passed = (date_now - date_bought).days
    # 日期和额度都不为零
    if yueka_days is not None:
        res_date = max(0, yueka_days - days_passed)
    else:
        res_date = 31  # 设置默认值为31好了
        
    if rate_value is not None:
        res_value = max(0, rate_value - count_value)
    else:
        res_value = 400 # 如果没有验证上，依然加默认值400额度

    # 获取功能
    boolean_fields = {k: v for k, v in user_limit.items() if isinstance(v, bool)}
    true_fields = [k for k, v in boolean_fields.items() if v]
    false_fields = [k for k, v in boolean_fields.items() if not v]
    # 功能重命名映射：
    field_names = {
    'auto_message': '主动发消息',
    'custom_identity': '自定义身份',
    'custom_action': '自定义动作',
    'voice': '语音功能',
    'sing': '唱歌功能',
    'meme': '表情包功能',
    'img_rec': '图像识别',
    'custom_sched': '自定义日程',
    'menstrual': '经期管理',
    'custom_sleep': '自定义睡眠',
    'auto_weather': '天气预报',
    'group': '群组管理',
    'game': '游戏功能',
    'custom': '自定义功能'
}
    version_mapping = {
    'free1': '免费版',
    'buy1': '付费版1',
    'buy2': '付费版2'
}
    boolean_fields = {k: v for k, v in user_limit.items() if k in field_names and v == 1}
    result = OrderedDict()

    if query_type in ['purchase']:
        result.update({
            'used_balance': f'已用额度：{count_value}',
            'remaining_balance': f'剩余额度：{res_value}',
            'purchase_date': f'购买日期：{date_value}',
            'remaining_days': f'剩余天数：{res_date}',
            'service_type': f'bot服务类型：{selected_version}',
            'current_date': f'当前日期：{current_date}'
        })
        return jsonify(result)
    elif query_type in ['feature']:
        user_info_collection = database['user_info']
        user_info = user_info_collection.find_one({"id": qq_id})
        if user_info:
            used_version = version_mapping.get(user_info.get('version'))
            result.update({
            'all_features':f'总功能数: {len(boolean_fields)}',
            'features': f'开启的功能: {", ".join([field_names[k] for k in boolean_fields])}',
            'version': f'当前版本：{used_version}'
            })
        if not user_info:
            result.update({
            'all_features':f'总功能数: {len(boolean_fields)}',
            'features': f'开启的功能: {", ".join([field_names[k] for k in boolean_fields])}',
            'version': f'当前版本：未知版本（需要先和bot对话后才可显示使用版本）'
            })
        return jsonify(result)
    else:
        return jsonify({'error': f'没有找到符合查询条件的数据'})


@app.route('/clear')
def clear_data():
    global output_data
    output_data = None
    return jsonify({'success': True})

@app.route('/select_version/<version>')
def select_version(version):
    global selected_version
    if selected_version == version:
        selected_version = None
    else:
        selected_version = version
    return jsonify({'success': True, 'selected_version': selected_version})

@app.route('/select_query_type/<query_type>')
def select_query_type(query_type):
    global selected_query_type
    if selected_query_type == query_type:
        selected_query_type = None
    else:
        selected_query_type = query_type
    return jsonify({'success': True, 'selected_query_type': selected_query_type})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)