'''
以下是更改特定数据库中特定表数据的代码
'''
import datetime

db_name_to_db = {
    # 光夜
    '00': '00DB',
    '11': '11DB',
    '55': '55DB',
    '66': '66DB',
    '77': '77DB',
    # 深空
    'ls': 'LS_DB',
    'qy': 'QY_DB',
    'sxh': 'SXH_DB',
    'xyz':'XYZ_DB',
    'qc': 'QC_DB',
    # 开发者个人测试数据库请在这里添加
    'cyxTest': 'TestDB'
}

bot_paths = {
    # 光夜
    '11': 'C:\\gaungye_bot\\ChatailoverBot11',
    '66': 'C:\\gaungye_bot\\ChatailoverBot66',
    '77': 'C:\\gaungye_bot\\ChatailoverBot77',
    '55': 'C:\\gaungye_bot\\ChatailoverBot55',
    '00': 'C:\\gaungye_bot\\ChatailoverBot00',
    # 深空
    'ls': 'C:\\0-shenkong_bot\\ls',
    'qy': 'C:\\0-shenkong_bot\\qy',
    'sxh': 'C:\\0-shenkong_bot\\sxh',
    'xyz': 'C:\\0-shenkong_bot\\xyz',
    'qc': 'C:\\0-shenkong_bot\\qc',
    # 开发者个人测试路径请在这里添加
    'cyxTest': 'D:\\AILover\\code\\loveBot1.2'
}

limit_data_default = {
    "id": 'default',
    "type": '默认',
    # 新用户默认20
    "rate": 20,
    "date": None,
    "days": None,
    "count": 0,
    "free_rate": 400, # 0629 新添加的，代表免费版用户拥有的额度
    "free_count":0, # 0629 新添加的，代表免费版用户已经使用的额度
    "wd_key": 'wd_key', # 0629 新添加的，代表用户最近一次购买信息验证的券码
    # 这里开始就是功能信息，bool值，仅有01
    "auto_message": 0,
    "custom_identity":1,
    "custom_action":1,
    "voice":0,
    "sing":0,
    "meme":0,
    "img_rec":0,
    "custom_sched":0,
    "menstrual":1,
    "custom_sleep":0,
    "auto_weather":0,
    "group":0,
    "game":1,
    "custom":0 # 0628 新添加的，代表用户是否是定制版用户/是否购买了定制版
}


'''
1. 新增信息：新增自定义信息 or 购买信息
'''

# 向xxDB的Info表里插入新数据：按需自定义待插入的数据库
def newInfo(client, user_qq= "default", user_name= "你的女朋友",user_info = "一名设计师", db_name = '00', info_data = None):
    '''
    db_name: default=='00'。可选值见db_name_to_db定义。
    info_data: 需要被插入的新数据，none则插入测试数据。
    '''
    # 连接男主数据库
    database = client[db_name_to_db[db_name]]
    info_collection = database['user_info']

    # 设置user_info表插入值
    if info_data == None:
        info_data = {
            "id": user_qq,
            "name": user_name,
            "info": user_info,
            "city": None,
            "city_code": None,   # 0702新添加的 数据格式是str
            "auto_message_on": 1,
            "custom_identity_on": 1,
            "custom_action_on": 1,
            "voice_on": 1,
            "sing_on": 1,
            "meme_on": 1,
            "img_rec_on": 1,
            "custom_sched_on": 1,
            "menstrual_on": 1,
            "custom_sleep_on": 1,
            "auto_weather_on": 1,
            "group_on": 1,
            "game_on": 1,
            "version": "buy1"
        }
    else:
        info_data = info_data
    #执行插入命令
    info_collection.insert_one(info_data)
    print("new data inserted in userInfo.")  # 新数据插入成功

    return info_data


# 向xxDB的Limit表里插入新数据：按需自定义待插入的数据库
def newLimit(client, user_qq= "default", type = "\u597d\u53cb", db_name = '00', limit_data = None):
    '''
    db_name: default=='00'。可选值见db_name_to_db定义。
    limit_data: 需要被插入的新数据，none则插入测试数据。
    '''
    # 连接男主数据库
    database = client[db_name_to_db[db_name]]
    limit_collection = database['user_limit']

    # 设置user_limit表插入值
    if limit_data == None:
        limit_data = {
            "id": user_qq,
            "type": type,
            # 新用户默认20
            "rate": 20,
            "date": None,
            "days": None,
            "count": 0,
            "free_rate": 400, # 0629 新添加的，代表免费版用户拥有的额度
            "free_count":0, # 0629 新添加的，代表免费版用户已经使用的额度
            "wd_key": 'wd_key', # 0629 新添加的，代表用户最近一次购买信息验证的券码
            # 这里开始就是功能信息，bool值，仅有01
            "auto_message": 0,
            "custom_identity":1,
            "custom_action":1,
            "voice":0,
            "sing":0,
            "meme":0,
            "img_rec":0,
            "custom_sched":0,
            "menstrual":1,
            "custom_sleep":0,
            "auto_weather":0,
            "group":0,
            "game":1,
            "custom":0 # 0628 新添加的，代表用户是否是定制版用户/是否购买了定制版
        }
    else:
        limit_data = limit_data

    limit_collection.insert_one(limit_data)
    
    print("new data inserted in userLimit.")  # 新数据插入成功

    return limit_data


'''
2. 查看购买信息：限制、使用量、免费版使用量
'''

def get_limit(collection, _type: str, qq: str):
    """获取限制"""
    entity = collection.find_one({"type": _type, "id": qq})
    # TODO bot 后端这里要改，找不到信息目前的后端应该init用户的新信息
    # 这个情况是 找不到用户的购买信息，相当于还是默认用户/未使用bot的用户，于是返回默认的限额，这里的使用量要设置未0
    if entity is None and qq != "默认":
        return collection.find_one({"type": _type, "id": "默认"})
    # 返回完整的数据结构
    return entity


'''
3. 修改购买信息

'''

# limit/rate 方面：一般是修改为固定值（购买月卡等操作） 改 rate & free_rate
def change_limit(collection, _type: str, qq: str, rate: int):
    """更新额度限制"""
    collection.update_one(
        {"type": _type, "id": qq},
        {"$set": {"type": _type, "id": qq, "rate": rate}},
        upsert=True,
    )

def change_free_limit(collection, _type: str, qq: str, rate: int):
    """更新额度限制"""
    collection.update_one(
        {"type": _type, "id": qq},
        {"$set": {"type": _type, "id": qq, "free_rate": rate}},
        upsert=True,
    )

# limit方面的 增加固定值（适用于额度补偿）
def add_limit(collection, _type: str, qq: str, amount: int):
    '''增加或者减少用户的额度限制rate，需要注意rate最小为0'''
    ori_usage = collection.find_one({"type": _type, "id": qq})
    if ori_usage.get('rate', 0) + amount <0:
        new_limit = 0
    else:
        new_limit = ori_usage.get('rate', 0) + amount
    collection.update_one(
        {"type": _type, "id": qq},
        {"$set": {"type": _type, "id": qq, "rate": new_limit}},
        upsert=True,
    )

def add_free_limit(collection, _type: str, qq: str, amount: int):
    '''增加或者减少用户的免费版额度限制free_rate，需要注意free_rate最小为0'''
    ori_usage = collection.find_one({"type": _type, "id": qq})
    if ori_usage.get('free_rate', 0) + amount <0:
        new_limit = 0
    else:
        new_limit = ori_usage.get('free_rate', 0) + amount
    collection.update_one(
        {"type": _type, "id": qq},
        {"$set": {"type": _type, "id": qq, "free_rate": new_limit}},
        upsert=True,
    )

# date方面：一般是修正购买日为今天 or 增改购买时长
def calculate_date(date):
    '''
    用于计算购买日期date 距离今天的差异
    '''
    # cookie实现的
    date_today = datetime.date.today()
    date_1 = datetime.date(date_today.year, date_today.month, date_today.day)
    date_buy = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    date_diff = date_1 - date_buy
    return date_diff.days

def change_date(collection, _type: str, qq: str, date = None, amount = 0):

    if date == None and amount == 0:
        return 
    if date == None:
        date = datetime.date.today()

    ori = collection.find_one({"type": _type, "id": qq})
    ori_days = ori.get('days', 31)
    collection.update_one(
        {"type": _type, "id": qq},
        {"$set": {"type": _type, "id": qq, "date": date, "days": ori_days + amount}},
        upsert=True,
    )

# usage方面：一般是增减固定值 改count & free_count
def add_usage(collection, _type: str, qq: str, amount: int):
    '''增加或者减少用户的使用量，需要注意使用量最小为0'''
    ori_usage = collection.find_one({"type": _type, "id": qq})
    if ori_usage.get('count', 0) + amount <0:
        new_usage = 0
    else:
        new_usage = ori_usage.get('count', 0) + amount
    collection.update_one(
        {"type": _type, "id": qq},
        {"$set": {"type": _type, "id": qq, "count": new_usage}},
        upsert=True,
    )

def add_free_usage(collection, _type: str, qq: str, amount: int):
    '''增加或者减少用户的使用量，需要注意使用量最小为0'''
    ori_usage = collection.find_one({"type": _type, "id": qq})
    if ori_usage.get('free_count', 0) + amount <0:
        new_usage = 0
    else:
        new_usage = ori_usage.get('free_count', 0) + amount
    collection.update_one(
        {"type": _type, "id": qq},
        {"$set": {"type": _type, "id": qq, "free_count": new_usage}},
        upsert=True,
    )

# 功能方面：修改功能权限
def add_function_permission(collection, _type: str, qq: str, fuction: str):
    ''' 添加某个功能为 有权限'''
    change_function_permission(collection, _type, qq, fuction, 1)

def change_function_permission(collection, _type: str, qq: str, fuction: str, access: bool):
    '''
    fuction可选项、默认值："auto_message": 0,
            "custom_identity":1,
            "custom_action":1,
            "voice":0,
            "sing":0,
            "meme":0,
            "img_rec":0,
            "custom_sched":0,
            "menstrual":1,
            "custom_sleep":0,
            "auto_weather":0,
            "group":0,
            "game":1,
            "custom":0 
    '''
    if fuction not in limit_data_default:
        raise Exception(f'fuction 参数错误，您传入的{fuction}不在可选项中')
    
    collection.update_one(
        {"type": _type, "id": qq},
        {"$set": {"type": _type, "id": qq, fuction: access}},
        upsert=True,
    )



'''
4. 未来：对于个性化信息的增改
'''
