'''
已弃用
'''

from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['compensationDB']

# 补偿所有用户
def compensate_all(master_name, user_id, days, amount):
    if user_id == 'all':
        result = db.users.update_many(
            { 'masterName': master_name },
            { '$inc': { 'days': int(days), 'amount': int(amount) } }
        )
    # 补充单一用户补偿的逻辑
    return result.modified_count

# 补偿特定用户
def compensate_user(master_name, user_id, days, amount):
    result = db.users.update_one(
        { 'masterName': master_name, 'user': user_id },
        { '$inc': { 'days': int(days), 'amount': int(amount) } }
    )
    return result.modified_count

# 节假日重置体验额度
def reset_holiday_mongo(master_name):
    result = db.users.update_many(
        { 'masterName': master_name },
        { '$set': { 'amount': 20 } }
    )
    return result.modified_count

# 查看用户自定义情况
def get_user_info(master_name, user_id):
    user_info = db.users.find_one({ 'masterName': master_name, 'user': user_id })
    return user_info

# 查看用户购买功能情况
def get_user_limit(master_name, user_id):
    user_limit = db.limits.find_one({ 'masterName': master_name, 'user': user_id })
    return user_limit

# 设置为‘主动版’
def set_active(master_name, user_id):
    result = db.limits.update_one(
        { 'masterName': master_name, 'user': user_id },
        { '$set': { 'version': 'active' } }
    )
    return result.modified_count

# 设置为‘定制版’
def set_custom(master_name, user_id):
    result = db.limits.update_one(
        { 'masterName': master_name, 'user': user_id },
        { '$set': { 'version': 'custom' } }
    )
    return result.modified_count

# 券码查找
def find_coupon_user(coupon_code):
    user = db.coupons.find_one({ 'coupon': coupon_code })
    return user
