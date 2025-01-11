import sys
# 将父目录添加到系统路径
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append("..")

from flask import Flask, request, jsonify,render_template
# from permission import *
# from wrapper import *
from mongo_client_init import *
import time
from backend.changeData import *

app = Flask(__name__)

# 定义数据库和类别的映射
cat_mapping = {
    "55": '55',
    "77": '77',
    "11": '11',
    "00": '00',
    "66": '66',
    # 深空
    "xi": 'sxh',
    "li": 'ls',
    "yu": 'qy',
    "qc": 'qc',
    # 恋与
    "lzy":'lzy'
}

# 定义额度的映射
amount_mapping = {
    "edu_50": 50,
    "edu_100": 100,
    "edu_200": 200,
}

# 0724更新 待测试
def write_jika(qq, category):

    print("qq:",qq, "正在write_jika")
    _type = "\u597d\u53cb"
    ''' 季卡逻辑：添加主动发消息 + 天数延长91天（不覆盖原本的购买信息）+ 添加1400额度'''
    # 根据category获取相应的数据库和额度
    if category[0:2] in cat_mapping or category[0:3] in cat_mapping:
        nanzhu = cat_mapping[category[0:3]]
        database = client[db_name_to_db[nanzhu]]
        limit_collection = database['user_limit']
        print(f"add {nanzhu} jika ...")

        # 添加主动发消息权限
        add_function_permission(limit_collection, _type = _type, qq=qq, fuction='auto_message')
        # 添加月卡天数和额度
        # 其实这个就是add_date 可以再封装一下
        change_date_1(limit_collection, _type, qq, 'today', 91, 'extend')
        add_limit(limit_collection, _type, qq, 1400)
    else:
        print(f"write_jika时遇到未知类别: {category}")
        print("开发者 write_jika(qq, category) 错误")
        
# 25/0111更新 新增lzy 将所有category[0:2]改为取category[0:2]或[0:3]
# 0724 更新 待测试
def write_permission(qq, category):

    print("qq:",qq, "正在write_permission")
    _type = "\u597d\u53cb"

    # 根据category获取相应的数据库和额度
    if category[0:2] in cat_mapping or category[0:3] in cat_mapping:
        nanzhu = cat_mapping[category[0:3]]
        database = client[db_name_to_db[nanzhu]]
        limit_collection = database['user_limit']
        print(f"add {nanzhu} card...")

        if category[-1] == '1':
            # 添加主动发消息权限
            add_function_permission(limit_collection, _type = _type, qq=qq, fuction='auto_message')
        # 添加月卡天数和额度+ 额度清0 
        change_usage(limit_collection, _type, qq, 0)
        if nanzhu in ['qc','55']:
            change_date(limit_collection, _type, qq, 'today', 60, 'cover')
            change_limit(limit_collection, _type, qq, 500)
        else:
            change_date(limit_collection, _type, qq, 'today', 31, 'cover')
            change_limit(limit_collection, _type, qq, 400)

    else:
        print(f"write_permission时遇到未知类别: {category}")
        print("开发者 write_permission(qq, category) 错误")

# 0718 修改的更为简明
def add_edu(qq, category):

    print("qq:",qq, "正在单独添加额度")

    _type = "\u597d\u53cb"

    # 处理类别
    if category[0:2] in cat_mapping or category[0:3] in cat_mapping:
        nanzhu = cat_mapping[category[0:3]]
        database = client[db_name_to_db[nanzhu]]
        limit_collection = database['user_limit']
        print(f"add {nanzhu} edu...")
        for key, value in amount_mapping.items():
            if key in category:
                add_limit(limit_collection, _type, qq, value)
                # rate_add_edu(usage_db, date_start_db, limit_db, qq, _type, value)
    else:
        print(f"添加额度时遇到未知类别: {category}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    qq = request.json.get('qq')
    category = request.json.get('category')
    key = request.json.get('key')

    #默认买月卡
    card_or_edu = "card"

    # 判断买的月卡还是额度：Replace the path below with the actual path to your txt files
    # 0724修改
    if category[-2] == '_' and (category[-1] in ['0', '1']):
        file_path = f'web_verify/txtfiles/{category}.txt'
        card_or_edu = "card"
     # 0909修：这里会报错跳到最后一步，读不到文件，粗糙小修一下
    elif category[-1] == 'a':
        file_path = f'web_verify/txtfiles/jika.txt'
        card_or_edu = "jika"
    else:
        file_path = f'web_verify/txtfiles/edu_keys_verify/{category}.txt'
        card_or_edu = "edu"

    # 打开对应的券的数据库
    try:
        with open(file_path, 'r') as file:
            keys = file.read().splitlines()
    except FileNotFoundError:
        print(f"开发者错误，无key文件路径！！{file_path}")
        return jsonify({'error': 'Invalid category'}), 400

    if key in keys:

        # 设置最大重试次数
        max_retries = 4
        # 设置重试之间的等待时间（秒）
        retry_interval = 0.1
        
        yichang_str = ""
        for retry_count in range(max_retries):
            try:
                if card_or_edu =="card":
                    # 添加月卡按钮后改这里
                    write_permission(qq, category)
                elif card_or_edu == "jika":
                    # 
                    write_jika(qq, category)
                else:
                    # 添加edu按钮后改这里
                    add_edu(qq,category)
                break
            except Exception as e:
                yichang_str = str(e)
                print(f"发生异常, 正在重试try")
            time.sleep(retry_interval)

            if retry_count == max_retries-1:
                print(f"发生异常: {yichang_str}\n 重试失败，用户权限未添加。key保留。")
                return jsonify({'verified': False}), 200
        
        # try成功的情况
        # todo:给这里加锁，我担心这个语句是不可并发的
        keys.remove(key)  # Remove the key from the list
        with open(file_path, 'w') as file:  # Open the file for writing
            file.write('\n'.join(keys))  # Write the updated list back to the file
        print("【success】")
        print("----------------")
        return jsonify({'verified': True}), 200
    else:
        print("key不在这个文件夹，【验证失败】", "qq:",qq)
        print("----------------")
        return jsonify({'verified': False}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)