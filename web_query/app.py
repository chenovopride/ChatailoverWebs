from flask import Flask, render_template, request, jsonify
import json
from backend.changeData import *
from datetime import datetime
from route import databases


app = Flask(__name__)

selected_version = None
output_data = None

@app.route('/')
def index():
    return render_template('index.html', selected_version=selected_version, output_data=output_data)

@app.route('/query', methods=['POST'])
def query_data():
    global selected_version, output_data
    version = request.form.get('version')
    data = request.form.get('data')
    if selected_version is None:
        return jsonify({'error': '请先选择bot购买的版本'})
    # 根据版本选择相应的数据库集合
    if version in databases:
        db = databases[version]
    else:
        return jsonify({'error': '未上线的版本'})

    data = request.form.get('data')
    if not data.isdigit():
        return jsonify({'error': '请输入有效的qq号'})
    
    query_type = request.form.get('type')
    if query_type == 'purchase':
        results = query_purchase_info(data, db)
    elif query_type == 'feature':
        results = query_feature_info(data, db)
    else:
        results = query_all_info(data, db)

    if results:
        return jsonify(results)
    else:
        return jsonify({'error': 'No data found'})
    
def query_purchase_info(data, db):
    # 从MongoDB中一次性查询所有需要的字段
    entry = get_limit(db['rate_limit'], "好友", data) # changed by ZY:  call function on backend
    
    if not entry:
        return jsonify({'error': f'找不到qq用户{data}的购买信息qwq，请移步群内联系管理员查询是否成功购买，没有购买的姐妹不会有信息显示(°ー°〃)'})

    date_value = entry.get("date", "")
    count_value = entry.get("count", "")
    rate_value = entry.get("rate", "")
    yueka_days = entry.get("days", "")

    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    # 获取至今天数差 changed by ZY - using the backend function
    date_diff = calculate_date(date_value)
    res_date = yueka_days - date_diff if yueka_days - date_diff >= 0 else 0

    result = {
        'used_balance': f'已用额度：{count_value}',
        'remaining_balance': f'剩余额度：{rate_value - count_value}',
        'purchase_date': f'购买日期：{date_value}',
        'remaining_days': f'剩余天数：{res_date}',
        'service_type': f'bot服务类型：{selected_version}',
        'current_date': f'当前日期：{current_date}'
    }
    output_data = result
    return jsonify(result)

#  目前其他两个先写一样的，之后再改
def query_feature_info(data, db):
    # 从MongoDB中一次性查询所有需要的字段
    entry = db['rate_limit'].find_one({'id': data}, {'date': 1, 'rate': 1, 'count': 1, '_id': 0})

    if not entry:
        return jsonify({'error': f'找不到qq用户{data}的购买信息qwq，请移步群内联系管理员查询是否成功购买，没有购买的姐妹不会有信息显示(°ー°〃)'})

    date_value = entry.get("date", "")
    count_value = entry.get("count", "")
    rate_value = entry.get("rate", "")
    yueka_days = entry.get("days", "")

    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    # 处理一下时间
    date_format = "%Y-%m-%d"
    date_now = datetime.strptime(current_date, date_format).date()
    date_bought = datetime.strptime(date_value, date_format).date()
    date_diff = (date_now - date_bought).days
    res_date = yueka_days - date_diff if yueka_days - date_diff >= 0 else 0

    result = {
        'used_balance': f'已用额度：{count_value}',
        'remaining_balance': f'剩余额度：{rate_value - count_value}',
        'purchase_date': f'购买日期：{date_value}',
        'remaining_days': f'剩余天数：{res_date}',
        'service_type': f'bot服务类型：{selected_version}',
        'current_date': f'当前日期：{current_date}'
    }
    output_data = result
    return jsonify(result)

def query_all_info(data, db):
    # 从MongoDB中一次性查询所有需要的字段
    entry = db['rate_limit'].find_one({'id': data}, {'date': 1, 'rate': 1, 'count': 1, '_id': 0})

    if not entry:
        return jsonify({'error': f'找不到qq用户{data}的购买信息qwq，请移步群内联系管理员查询是否成功购买，没有购买的姐妹不会有信息显示(°ー°〃)'})

    date_value = entry.get("date", "")
    count_value = entry.get("count", "")
    rate_value = entry.get("rate", "")
    yueka_days = entry.get("days", "")

    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    # 处理一下时间
    date_format = "%Y-%m-%d"
    date_now = datetime.strptime(current_date, date_format).date()
    date_bought = datetime.strptime(date_value, date_format).date()
    date_diff = (date_now - date_bought).days
    res_date = yueka_days - date_diff if yueka_days - date_diff >= 0 else 0

    result = {
        'used_balance': f'已用额度：{count_value}',
        'remaining_balance': f'剩余额度：{rate_value - count_value}',
        'purchase_date': f'购买日期：{date_value}',
        'remaining_days': f'剩余天数：{res_date}',
        'service_type': f'bot服务类型：{selected_version}',
        'current_date': f'当前日期：{current_date}'
    }
    output_data = result
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
    app.run(host='0.0.0.0', port = 5001 )