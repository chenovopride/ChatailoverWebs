from flask import Flask, request, jsonify,render_template
from permission import *
from wrapper import *
from mongo_client_init import *
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
    "yu": 'qy'
}

# 定义额度的映射
amount_mapping = {
    "edu_50": 50,
    "edu_100": 100,
    "edu_200": 200,
}


def write_jika(qq, category):

    _type = "\u597d\u53cb"
    # 因为有人可能没有月卡直接买季卡，所以这里必须是01
    jika_rate = 1401
    print("qq:",qq, "正在添入【季卡】稳定版权限")

    if category == "jika_55":
        
        # 更新购买日期, 天数在原本的基础上延长
        jika_date_update(date_start_db_55, qq)
        # 新函数，不能直接使用原本的rate_add_edu，原因是rate_add_edu如果
        rate_add_edu_with_card(limit_db_55, usage_db_55, qq, jika_rate, _type)

    elif category == "jika_00":
        jika_date_update(date_start_db_00, qq)
        rate_add_edu_with_card(limit_db_00, usage_db_00, qq, jika_rate, _type)


    elif category == "jika_66":

        jika_date_update(date_start_db_66, qq)
        # 更新购买日期
        rate_add_edu_with_card(limit_db_66, usage_db_66, qq, jika_rate, _type)

    elif category == "jika_77":
        jika_date_update(date_start_db_77, qq)

        rate_add_edu_with_card(limit_db_77, usage_db_77, qq, jika_rate, _type)

    elif category == "jika_11":

        jika_date_update(date_start_db_11, qq)

        rate_add_edu_with_card(limit_db_11, usage_db_11, qq, jika_rate, _type)

    else:
        print("开发者错误，错误在 write_jika")

def write_permission(qq, category):

    _type = "\u597d\u53cb"
    wending_rate_55 = 400
    # wending_rate_55 = 600
    # wending_rate_glm = 76000
    # zhudong_rate_glm = 80000
    wending_rate_ft = 400
    zhudong_rate_520 = 401
    print("qq:",qq, "正在添入稳定版权限")

    #光夜bot月卡
    if category == "Category5_0":
        # 更新rate
        # usage清0，并且额度变为月卡额度
        rate_update(limit_db_55,usage_db_55, qq, wending_rate_55, _type)
        # 更新购买日期
        date_update(date_start_db_55, qq)

    elif category == "Category5_1":
        # 更新rate
        rate_update(limit_db_55, usage_db_55, qq, zhudong_rate_520, _type)
        # 更新购买日期
        date_update(date_start_db_55, qq)

    elif category == "Category0_0":
        # 更新rate
        rate_update(limit_db_00,usage_db_00, qq, wending_rate_ft, _type)
        # 更新购买日期
        date_update(date_start_db_00, qq)

    elif category == "Category0_1":
        # 更新rate
        rate_update(limit_db_00,usage_db_00, qq, zhudong_rate_520, _type)
        # 更新购买日期
        date_update(date_start_db_00, qq)

    elif category == "Category6_0":
        # 更新rate
        rate_update(limit_db_66,usage_db_66, qq, wending_rate_ft, _type)
        # 更新购买日期
        date_update(date_start_db_66, qq)

    elif category == "Category6_1":
        # 更新rate
        rate_update(limit_db_66,usage_db_66, qq, zhudong_rate_520, _type)
        # 更新购买日期
        date_update(date_start_db_66, qq)

    elif category == "Category7_0":
        # 更新rate
        rate_update(limit_db_77,usage_db_77, qq, wending_rate_ft, _type)
        # 更新购买日期
        date_update(date_start_db_77, qq)

    elif category == "Category7_1":
        # 更新rate
        rate_update(limit_db_77,usage_db_77, qq, zhudong_rate_520, _type)
        # 更新购买日期
        date_update(date_start_db_77, qq)

    elif category == "Category1_0":
        # 更新rate
        rate_update(limit_db_11,usage_db_11, qq, wending_rate_ft, _type)
        # 更新购买日期
        date_update(date_start_db_11, qq)

    elif category == "Category1_1":
        # 更新rate
        rate_update(limit_db_11,usage_db_11, qq, zhudong_rate_520, _type)
        # 更新购买日期
        date_update(date_start_db_11, qq)

    # 深空bot月卡：
    #⭐
    elif category == "CategoryXing":
        # 更新rate
        rate_update(limit_db_xing,usage_db_xing, qq, zhudong_rate_520, _type)
        # 更新购买日期
        date_update(date_start_db_xing, qq)
    #🍐
    elif category == "CategoryLi":
        # 更新rate
        rate_update(limit_db_li,usage_db_li, qq, zhudong_rate_520, _type)
        # 更新购买日期
        date_update(date_start_db_li, qq)
    #🐟
    elif category == "CategoryYu":
        # 更新rate
        rate_update(limit_db_yu,usage_db_yu, qq, zhudong_rate_520, _type)
        # 更新购买日期
        date_update(date_start_db_yu, qq)

    else:
        print("遇到了一些问题？请群内反馈~")

# 0718 修改的更为简明
def add_edu(qq, category):

    print("qq:",qq, "正在单独添加额度")

    _type = "\u597d\u53cb"

    # 处理类别
    if category[0:2] in cat_mapping:
        nanzhu = cat_mapping[category[0:2]]
        database = client[db_name_to_db[nanzhu]]
        limit_collection = database['user_limit']
        print(f"add {nanzhu} edu...")

        for key, value in amount_mapping.items():
            if key in category:
                change_limit(limit_collection, _type, qq, value)
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
    if category[0:3] == 'Cat':
        file_path = f'txtfiles/{category}.txt'
        card_or_edu = "card"
    elif category[0:4] == 'jika':
        file_path = f'txtfiles/jika.txt'
        card_or_edu = "jika" 
    else:
        file_path = f'txtfiles/edu_keys_verify/{category}.txt'
        card_or_edu = "edu"

    # 打开对应的券的数据库
    try:
        with open(file_path, 'r') as file:
            keys = file.read().splitlines()
    except FileNotFoundError:
        print("开发者错误，无key文件路径！！")
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
