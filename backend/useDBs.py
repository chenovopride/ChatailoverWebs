
#以下是初始化光夜+深空数据库代码

def newGuangyeDB(client):
# 创建光夜5男主数据库，均插入初始数据
    function_00db = client['00DB']
    function_77db = client['77DB']
    function_55db = client['55DB']
    function_66db = client['66DB']
    function_11db = client['11DB']
# 创建 user_info 集合并插入初始数据
    info_collection00 = function_00db['user_info']
    info_collection77 = function_77db['user_info']
    info_collection55 = function_55db['user_info']
    info_collection66 = function_66db['user_info']
    info_collection11 = function_11db['user_info']
# 设置user_info表插入值
    info_data = {
        "id": "921365773",
        "name": "test1",
        "info": "机器人",
        "city": "美国,加利福尼亚州,洛杉矶",
        "city_code": None,
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
        "version": "free1"
}
#执行初始化光夜男主DB命令
    info_collection00.insert_one(info_data)
    info_collection77.insert_one(info_data)
    info_collection55.insert_one(info_data)
    info_collection66.insert_one(info_data)
    info_collection11.insert_one(info_data)

# 同理创建 user_limit 集合并插入初始数据
    limit_collection00 = function_00db['user_limit']
    limit_collection77 = function_77db['user_limit']
    limit_collection55 = function_55db['user_limit']
    limit_collection66 = function_66db['user_limit']
    limit_collection11 = function_11db['user_limit']
# 设置user_limit表插入值
    limit_data = {
        "id": "921365773",
        "type": "friends",
        "rate": None,
        "date": None,
        "days": None,
        "count": 0,
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
    limit_collection00.insert_one(limit_data)
    limit_collection77.insert_one(limit_data)
    limit_collection55.insert_one(limit_data)
    limit_collection66.insert_one(limit_data)
    limit_collection11.insert_one(limit_data)
    
# 打印确认信息
    print("guangyeDB and collections created successfully.")




def newShenkongDB(client):
# 创建深空5男主数据库，均插入初始数据
    QYdb = client['QY_DB']
    SXHdb = client['SXH_DB']
    LSdb = client['LS_DB']
    XYZdb = client['XYZ_DB']
    QCdb = client['QC_DB']
# 创建 user_info 集合并插入初始数据
    info_collectionQY = QYdb['user_info']
    info_collectionSXH = SXHdb['user_info']
    info_collectionLS = LSdb['user_info']
    info_collectionXYZ = XYZdb['user_info']
    info_collectionQC = QCdb['user_info']
# 设置user_info表默认值
    info_data = {
        "id": "921365773",
        "name": "test1",
        "info": "机器人",
        "city": "美国,加利福尼亚州,洛杉矶",
        "city_code": None,
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
        "version": "free1"
}
#执行初始化光夜男主DB命令
    info_collectionQY.insert_one(info_data)
    info_collectionSXH.insert_one(info_data)
    info_collectionLS.insert_one(info_data)
    info_collectionXYZ.insert_one(info_data)
    info_collectionQC.insert_one(info_data)

# 同理创建 user_limit 集合并插入初始数据
    limit_collectionQY = QYdb['user_limit']
    limit_collectionSXH = SXHdb['user_limit']
    limit_collectionLS = LSdb['user_limit']
    limit_collectionXYZ = XYZdb['user_limit']
    limit_collectionQC = QCdb['user_limit']
# 设置user_limit表默认值
    limit_data = {
        "id": "921365773",
        "type": "friends",
        "rate": None,
        "date": None,
        "days": None,
        "count": 0,
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
    limit_collectionQY.insert_one(limit_data)
    limit_collectionSXH.insert_one(limit_data)
    limit_collectionLS.insert_one(limit_data)
    limit_collectionXYZ.insert_one(limit_data)
    limit_collectionQC.insert_one(limit_data)
    
# 打印确认信息
    print("shekongDB and collections created successfully.")


