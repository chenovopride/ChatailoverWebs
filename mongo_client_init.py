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