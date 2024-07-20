
from backend.changeData import *
from backend_tinydb import *

'''CYX测试路径'''
# date_start_db = TinyDB(r"D:\AILover\code\loveBot1.2\chatgpt\data\date_start.json")
# usage_db = TinyDB(r"D:\AILover\code\loveBot1.2\chatgpt\data\rate_usage.json")
# limit_db = TinyDB(r"D:\AILover\code\loveBot1.2\chatgpt\data\rate_limit.json")

# limit_db_55 = limit_db
# limit_db_00 = limit_db
# limit_db_66 = limit_db
# limit_db_77 = limit_db
# limit_db_11 = limit_db
# usage_db_55 = usage_db
# usage_db_00 = usage_db
# usage_db_66 = usage_db
# usage_db_77 = usage_db
# usage_db_11 = usage_db
# date_start_db_55 = date_start_db
# date_start_db_00 = date_start_db
# date_start_db_66 = date_start_db
# date_start_db_77 = date_start_db
# date_start_db_11 = date_start_db


''' 服务器路径'''
limit_db_55 = TinyDB(r"C:\gaungye_bot\ChatailoverBot55\chatgpt\data\rate_limit.json")
limit_db_00 = TinyDB(r"C:\gaungye_bot\ChatailoverBot00\chatgpt\data\rate_limit.json")
limit_db_66 = TinyDB(r"C:\gaungye_bot\ChatailoverBot66\chatgpt\data\rate_limit.json")
limit_db_77 = TinyDB(r"C:\gaungye_bot\ChatailoverBot77\chatgpt\data\rate_limit.json")
limit_db_11 = TinyDB(r"C:\gaungye_bot\ChatailoverBot11\chatgpt\data\rate_limit.json")

usage_db_55 = TinyDB(r"C:\gaungye_bot\ChatailoverBot55\chatgpt\data\rate_usage.json")
usage_db_00 = TinyDB(r"C:\gaungye_bot\ChatailoverBot00\chatgpt\data\rate_usage.json")
usage_db_66 = TinyDB(r"C:\gaungye_bot\ChatailoverBot66\chatgpt\data\rate_usage.json")
usage_db_77 = TinyDB(r"C:\gaungye_bot\ChatailoverBot77\chatgpt\data\rate_usage.json")
usage_db_11 = TinyDB(r"C:\gaungye_bot\ChatailoverBot11\chatgpt\data\rate_usage.json")

date_start_db_55 = TinyDB(r"C:\gaungye_bot\ChatailoverBot55\chatgpt\data\date_start.json")
date_start_db_00 = TinyDB(r"C:\gaungye_bot\ChatailoverBot00\chatgpt\data\date_start.json")
date_start_db_66 = TinyDB(r"C:\gaungye_bot\ChatailoverBot66\chatgpt\data\date_start.json")
date_start_db_77 = TinyDB(r"C:\gaungye_bot\ChatailoverBot77\chatgpt\data\date_start.json")
date_start_db_11 = TinyDB(r"C:\gaungye_bot\ChatailoverBot11\chatgpt\data\date_start.json")


date_db_for = {
    '00': date_start_db_00,
    '55': date_start_db_55,
    '66': date_start_db_66,
    '77': date_start_db_77,
    '11': date_start_db_11
}

limit_db_for = {
    '00': limit_db_00,
    '55': limit_db_55,
    '66': limit_db_66,
    '77': limit_db_77,
    '11': limit_db_11
}

def compensate( man, user_id, days_all, amount_all, backend ='mongodb'):

    if backend not in ['mongodb', 'tinydb']:
        print('backend设置错误！')
        return False
    
    date_status = True
    rate_status = True

    if backend == 'tinydb':
        if user_id == 'all':
            # 所有用户补偿
            if days_all!= 0:
                date_status = date_add_num(date_db_for[man], days_all)
            if amount_all!=0:
                rate_status = rate_add_num(limit_db_for[man], amount_all)
        else:
            # 给特定用户补偿
            if days_all!= 0:
                date_status = date_add_num_for_qq(date_db_for[man], days_all, user_id)
            if amount_all!=0:
                rate_status = rate_add_num_for_qq(limit_db_for[man], amount_all, user_id)
        print('date_status and rate_status:', date_status ,rate_status)
        return (date_status and rate_status)
    else:
        print('mongo后端还未实现')
        return False
        
    
def reset_holiday(game, gift_limit_count = 20, backend ='mongodb'):
    
    if backend not in ['mongodb', 'tinydb']:
        print('backend设置错误！')
        return False
    
    if backend == 'tinydb':
        if game == '光夜':
            reset20(usage_db_00)
            reset20(usage_db_11)
            reset20(usage_db_55)
            reset20(usage_db_66)
            reset20(usage_db_77)
            return True
        else:
            print('还未上线！')
            return False
    else:
        print('还未上线！')
        return False






    

