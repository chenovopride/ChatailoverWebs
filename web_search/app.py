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

# cat_mapping = {


# }

@app.route('/')
def index():
    return render_template('index.html', selected_version=selected_version, output_data=output_data)

@app.route('/query', methods=['POST'])
def query_balance():
    global selected_version, output_data
    version = request.form.get('version')
    qq_id = request.form.get('data')
    # query_type = request.form.get('type')
    #想实现的效果：query_type为a查询额度，为b查询功能，为c查询所有，默认为c
    query_type = request.form.get('type', 'a')  # 设置默认值
    
    if not qq_id.isdigit():
        return jsonify({'error': '请输入有效的qq号'})

    if selected_version is None:
        return jsonify({'error': '请先选择bot购买的版本'})
    
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
    user_info_collection = database['user_info']

    # 服务器注释 
    # print(f'Debug: user_limit_collection = {user_limit_collection}')
    # print(f'Debug: user_info_collection = {user_info_collection}')
    
    if user_limit_collection is None or user_info_collection is None:
        return jsonify({'error': '集合不存在，请确认数据库配置'})
    
    # 查询user_limit表
    user_limit = user_limit_collection.find_one({"id": qq_id})
    print('user_limit: ',user_limit)
    if not user_limit:
        return jsonify({'error': f'找不到qq用户{qq_id}的购买信息，请联系管理员确认购买情况'})

    result = {}
    
    if query_type in ['a']:
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

        # calculate_date(date)

        if yueka_days is not None:
            res_date = max(0, yueka_days - days_passed)
        else:
            res_date = 31  # 设置默认值为31好了
        # res_date = max(0, yueka_days - days_passed)
        
        result = OrderedDict()
        result.update({
            'used_balance': f'已用额度：{count_value}',
            'remaining_balance': f'剩余额度：{rate_value - count_value}',
            'purchase_date': f'购买日期：{date_value}',
            'remaining_days': f'剩余天数：{res_date}',
            'service_type': f'bot服务类型：{selected_version}',
            'current_date': f'当前日期：{current_date}'
        })

    if query_type in ['b']:
        user_info = user_info_collection.find_one({"id": qq_id})
        if user_info:
            boolean_fields = {k: v for k, v in user_info.items() if isinstance(v, bool)}
            true_fields = [k for k, v in boolean_fields.items() if v]
            false_fields = [k for k, v in boolean_fields.items() if not v]
            
            result = OrderedDict()
            result.update({
                'true_fields': f'已开通功能数量：{len(true_fields)}',
                'true_fields_name': f'已开通功能：{", ".join(true_fields)}',
                'false_fields': f'未开通功能数量：{len(false_fields)}',
                'false_field_names': f'未开通功能：{", ".join(false_fields)}'
            })

    if query_type in ['c']:
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
        if yueka_days is not None:
            res_date = max(0, yueka_days - days_passed)
        else:
            res_date = 31  # 设置默认值为31好了

        user_info = user_info_collection.find_one({"id": qq_id})
        if user_info:
            boolean_fields = {k: v for k, v in user_info.items() if isinstance(v, bool)}
            true_fields = [k for k, v in boolean_fields.items() if v]
            false_fields = [k for k, v in boolean_fields.items() if not v]

        result = OrderedDict()
        result.update({
        'used_balance': f'已用额度：{count_value}',
        'remaining_balance': f'剩余额度：{rate_value - count_value}',
        'purchase_date': f'购买日期：{date_value}',
        'remaining_days': f'剩余天数：{res_date}',
        'service_type': f'bot服务类型：{selected_version}',
        'current_date': f'当前日期：{current_date}',
        'false_fields_count': f'未开通功能数量：{len(false_fields)}',
        'false_field_names': f'未开通功能：{", ".join(false_fields)}',
        'true_fields_count': f'已开通功能数量：{len(true_fields)}',
        'true_field_names': f'已开通功能：{", ".join(true_fields)}'
        })
        
        # 定义希望的顺序
        order = ['used_balance', 'remaining_balance', 'purchase_date', 'remaining_days', 
         'service_type', 'current_date', 'false_fields_count', 'false_field_names', 
         'true_fields_count', 'true_field_names']
        # 创建一个按照 order 顺序排列的 OrderedDict
        ordered_result = OrderedDict((key, result[key]) for key in order if key in result)

        # 这里print显示排序成功了也对result重新赋值了，但是最后网页显示的结果却依然乱序？
        result = ordered_result
        # print(result)
    
    if not result:
        return jsonify({'error': '没有找到符合查询条件的数据'})
    
    return jsonify(result)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)