import json
import os
from tinydb import TinyDB, Query
from backend.changeData import *
'''
以下是:
    1. 旧数据库移到MongoDB中的代码
    2. 旧数据库合并为新数据格式的代码
'''


def oldMove_Date(client):
# 读取JSON文件
# 替换为远程数据库路径
    # file_path = 'D:/AudioModel/web_tst/66/date_start.json'
    # CYX 测试地址 测试地址
    file_path = "D:\AILover\code\AIChatWeb_verify\data\date_start.json"
    with open(file_path, 'r') as file:
        data = json.load(file)
    db00 = client['00DB']
    db77 = client['77DB']
    db55 = client['55DB']
    db66 = client['66DB']
    db11 = client['11DB']
    QYdb = client['QY_DB']
    SXHdb = client['SXH_DB']
    LSdb = client['LS_DB']
    XYZdb = client['XYZ_DB']
    QCdb = client['QC_DB']
    collection00 = db00['date_start']
    collection77 = db77['date_start']
    collection55 = db55['date_start']
    collection66 = db66['date_start']
    collection11 = db11['date_start']
    collectionQY = QYdb['date_start']
    collectionSXH = SXHdb['date_start']
    collectionLS = LSdb['date_start']
    collectionXYZ = XYZdb['date_start']
    collectionQC = QCdb['date_start']
# 遍历JSON数据并插入到数据库
    for key, value in data["_default"].items():
        doc = {
        "id": value.get("id", ""),
        "date": value.get("date", ""),
        "days": value.get("left", 0),  # 将原本left字段转为days
        "type": "friends"  # 新插入的字段，如果不需要可以扔掉
    }
# 这样写累赘，但只用一次就不重构了
        collection00.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection77.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection55.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection66.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection11.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )      
        
        collectionQY.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionSXH.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionLS.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionXYZ.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionQC.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
# 关闭MongoDB连接
    client.close()

def oldMove_Limit(client):
    # 读取JSON文件
    # 替换为远程数据库路径
    # file_path = 'D:/AudioModel/web_tst/66/rate_limit.json'
    # CYX 测试地址
    file_path = r"D:\AILover\code\AIChatWeb_verify\data\rate_limit.json"
    with open(file_path, 'r') as file:
        data = json.load(file)
    db00 = client['00DB']
    db77 = client['77DB']
    db55 = client['55DB']
    db66 = client['66DB']
    db11 = client['11DB']
    QYdb = client['QY_DB']
    SXHdb = client['SXH_DB']
    LSdb = client['LS_DB']
    XYZdb = client['XYZ_DB']
    QCdb = client['QC_DB']
    collection00 = db00['rate_limit']
    collection77 = db77['rate_limit']
    collection55 = db55['rate_limit']
    collection66 = db66['rate_limit']
    collection11 = db11['rate_limit']
    collectionQY = QYdb['rate_limit']
    collectionSXH = SXHdb['rate_limit']
    collectionLS = LSdb['rate_limit']
    collectionXYZ = XYZdb['rate_limit']
    collectionQC = QCdb['rate_limit']
# 遍历JSON数据并插入到数据库
    for key, value in data["_default"].items():
        doc = {
        "id": value.get("id", ""),
        "rate": value.get("rate", ""),
        "type": value.get("type", "")
    }
# 这样写累赘，但只用一次就不重构了
        collection00.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection77.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection55.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection66.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection11.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )      
        
        collectionQY.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionSXH.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionLS.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionXYZ.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionQC.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
# 关闭MongoDB连接
    client.close()

def oldMove_Usage(client):
# 读取JSON文件
# 替换为远程数据库路径
    file_path = 'D:/AudioModel/web_tst/66/rate_usage.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    db00 = client['00DB']
    db77 = client['77DB']
    db55 = client['55DB']
    db66 = client['66DB']
    db11 = client['11DB']
    QYdb = client['QY_DB']
    SXHdb = client['SXH_DB']
    LSdb = client['LS_DB']
    XYZdb = client['XYZ_DB']
    QCdb = client['QC_DB']
    collection00 = db00['rate_usage']
    collection77 = db77['rate_usage']
    collection55 = db55['rate_usage']
    collection66 = db66['rate_usage']
    collection11 = db11['rate_usage']
    collectionQY = QYdb['rate_usage']
    collectionSXH = SXHdb['rate_usage']
    collectionLS = LSdb['rate_usage']
    collectionXYZ = XYZdb['rate_usage']
    collectionQC = QCdb['rate_usage']
# 遍历JSON数据并插入到数据库
    for key, value in data["_default"].items():
        doc = {
        "id": value.get("id", ""),
        "count": value.get("count", ""),
        "type": value.get("type", ""),
        "time": value.get("time", ""),
        "day": value.get("day", "")  # 看远程新出现的字段，不知何用但加上了
    }
# 这样写累赘，但只用一次就不重构了
        collection00.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection77.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection55.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection66.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
        collection11.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )      
        
        collectionQY.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionSXH.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionLS.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionXYZ.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )   
        collectionQC.update_one(
        {"id": doc["id"]},  # 使用id作为唯一标识进行插入或更新
        {"$set": doc},
        upsert=True
    )
# 关闭MongoDB连接
    client.close()

# 函数作用：将原本男主的用户购买信息同步到mongodb中
# 实现思路：根据男主名称，判断原本男主的数据路径以及mongo对应的数据路径，从而完成迁移
def old_merge_user_limit(client, bot_name = '00'):
    '''
    bot_name: 00, 11, 55, 66, 77, sxh, ls, qy, qc, xyz, cyxTest
    
    '''

    base_path = bot_paths[bot_name]
    
    # 默认limit_file_path: C:\gaungye_bot\ChatailoverBot00\data\rate_limit.json
    limit_file_path = os.path.join(base_path, r'chatgpt\data\rate_limit.json')
    usage_file_path = os.path.join(base_path, r'chatgpt\data\rate_usage.json')
    date_file_path = os.path.join(base_path, r'chatgpt\data\date_start.json')

    limit_db = TinyDB(limit_file_path)
    usage_db = TinyDB(usage_file_path)
    date_db = TinyDB(date_file_path)
    q = Query()

    # 遍历limit里面的数据，因为usage太多了还有免费版, date 里面又没有记录仅有额度的人的信息, 所以便利limit

    # file_path = r"D:\AILover\code\AIChatWeb_verify\data\rate_limit.json"
    file_path = limit_file_path
    with open(file_path, 'r') as file:
        data = json.load(file)

    for key, value in data["_default"].items():

        # 获得原始的 limit
        user_qq = value.get("id", "")
        user_rate = value.get("rate", "")
        user_type = value.get("type", "")
        print(f'迁移用户：{user_qq} 的数据中...')

        # 获得原始的 usage
        usage_for_qq = usage_db.get(q.fragment({"type": user_type, "id": user_qq}))
        if usage_for_qq == None:
            user_usage = 0
        else:
            user_usage = usage_for_qq["count"]
        print(f'    usage为{user_usage}...')

        # 获得原始的 date
        date_for_qq = date_db.get(q.fragment({"id": user_qq}))
        if date_for_qq == None:
            user_date = "2024-06-29"
            user_days = 35
        else:
            user_date = date_for_qq["date"]
            user_days = date_for_qq["left"]
        print(f'    user_date为{user_date}...')
        print(f'    user_days为{user_days}...')

        user_new_limit = {
            "id": user_qq,
            "type": user_type,
            "rate": user_rate,
            "date": user_date,
            "days": user_days,
            "count": user_usage,
            "free_rate": 400, 
            "free_count":0,
            "wd_key": 'wd_key',
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
            "custom":0
        }
        
        newLimit(client, db_name = bot_name, limit_data = user_new_limit)

        print(f'    用户：{user_qq} 的数据已经迁移到mongodb！')
        print('---')


# 函数作用：将原本男主的用户info自定义信息同步到mongodb中
# 实现思路：根据男主名称，判断原本男主的info数据路径以及mongo对应的数据路径，从而完成迁移
def old_merge_user_info(client, bot_name = '00'):
    '''
    bot_name: 00, 11, 55, 66, 77, sxh, ls, qy, qc, xyz, cyxTest
    
    '''
    # 获得 bot_name 的老用户数据
    base_path = bot_paths[bot_name]

    # 原始用户自定义数据库路径, 例如 C:\gaungye_bot\ChatailoverBot66\chatgpt\data\user_info
    old_info_dir = os.path.join(base_path, r'chatgpt\data\user_info')

    for file_name in os.listdir(old_info_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(old_info_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # print(f"File Name: {file_name}")
                # print(f"User QQ: {file_name.split('.json')[0]}")
                # 获取原始的用户信息
                user_qq = file_name.split('.json')[0]
                user_name = data.get("name", None)
                user_intro = data.get("intro", None)
                # 注意这里的 user_city_id 也是str类型
                user_city_id = data.get("city_id", None) # 查不到就记为None，在mongo里面显示为null。

                print(f'迁移用户：{user_qq} 的数据中...')

                info_data = {
                    "id": user_qq,
                    "name": user_name,
                    "info": user_intro,
                    "city": None,
                    "city_code": user_city_id,
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

                # 增加到 bot_name 新的数据库中
                newInfo(client, db_name = bot_name, info_data = info_data)