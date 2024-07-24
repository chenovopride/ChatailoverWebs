from pymongo import MongoClient
from datetime import datetime
from backend.useDBs import *
from backend.moveOld import *
from backend.changeData import *


# 连接到MongoDB服务器
username = 'rootUser'
password = 'ChatAILover'
auth_db = 'admin' #可以新建其他的数据库,admin会存储所有数据库包括config等,不建议直接在admin
# client = MongoClient(f'mongodb://{username}:{password}@localhost:27017/{auth_db}')

# CYX 测试地址
client = MongoClient('mongodb://localhost:27017/')

# ## MoveOld（只用一次）
# # 因为每次移动完后都会关掉数据库，所以不要一次性运行三个，会失效，挨个运行。
# oldMove_Date(client)  # 将date_start转入MongoDB内
# oldMove_Limit(client)  # 将rate_limit转入MongoDB内
# oldMove_Usage(client)  # 将rate_usage转入MongoDB内


'''
老用户购买数据和个性化数据迁移
'''
# 个人测试的用法
# old_merge_user_limit(client, bot_name='cyxTest')
# old_merge_user_info(client, bot_name='cyxTest')

# # UseDBs
# newGuangyeDB(client)  # 初始化新数据库（光夜）
# newShenkongDB(client)  #初始化新数据库（深空）

# # ChangeData
# 0627 这两个函数修改了一下
# newInfo(client)  # 写入新user_info数据
# newLimit(client)  # 写入新user_limit数据
# changeFields(client)  # 改变/增加数据储存字段
# # # 向xx数据库新增表————更改代码行xxcollection = xxdb['xx表']，即可新建，表名为‘xx表’


import datetime


# limit_db_55 = TinyDB(r"C:\Windows-quickstart-go-cqhttp-refs.tags.55bot\chatgpt\data\rate_limit.json")

# # mon_card_remain_days(date_start_db_55, "18392440042")
# _type = "\u597d\u53cb"
# # wending_rate_55 = 600



# rate_update(limit_db_55,usage_db_55, "1832292582", 601, _type)
# date_update(date_start_db_55, "1832292582")

a = datetime.date.today()
print(a)
