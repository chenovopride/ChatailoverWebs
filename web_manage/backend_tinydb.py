import time
from tinydb import TinyDB, Query
from tinydb.operations import increment
from tinydb.table import Document
import datetime
from datetime import datetime
import json

'''
1. 使用了rate_limit里面的几个函数，方便计算补偿额度（天数）
2. 目前提供了四种函数，四个主函数均有注释，包含了较多情况，请选择使用，不要重复造轮子
'''


        
def date_fix(date_db,_id, ori_left, fix_left):

    Q = Query()
    date = str(datetime.date.today())
    date_and_id = date_db.search(Q.id == _id)
    date_ = date_and_id[0]["date"]
    used = Calculate_date(date_)
    limit = date_and_id[0]["left"]
    if limit == ori_left:
        date_db.update(({"left" : fix_left}), (Q.id == _id))

def Calculate_date(date):
    # print(date)
    date_today = datetime.date.today()
    date_today = str(date_today).split("-")
    date_1 = datetime.date(int(date_today[0]), int(date_today[1]), int(date_today[2]))
    date_buy = str(date).split("-")
    date_2 = datetime.date(int(date_buy[0]), int(date_buy[1]), int(date_buy[2]))
    date_3 = date_1 - date_2
    date_3 = str(date_3).split(" ")
    # print(date_1)
    # print(date_2)
    # print(date_3)
    if date_3[0] == '0:00:00':
        res = 0
    else:
        res = int(date_3[0])
        
    return res


def fix_add_days(date_db, ori_left, fix_left):
    '''
    将月卡天数为 ori_left 的用户的月卡天数变为 fix_left
    '''
    #list_1 = date_start.all()
    #print(list_1)
    for user in date_db:
        #print(1)
        #print(user)
        date_fix(user["id"], ori_left, fix_left)
        


def rate_add_num(db, num):
    '''
    将rate_limit中,所有用户的rate限制增加num条
    '''
    # 获取默认表格
    table = db.table('_default')
    q = Query()
    try:
        # 遍历每个记录并检查id是否全部为数字字符,排除给“默认”增加额度的情况
        for record in table.all():
            print("rate_add_num 额度补偿了用户:", record)
            if 'id' in record and str(record['id']).isdigit():
                # print("true")
                _type = record['type']
                qq = record['id']
                new_limit = record['rate'] + num
                db.upsert({"type": _type, "id": qq, "rate": new_limit}, q.fragment({"type": _type, "id": qq}))
            else:
                print("*")
    except Exception as e:
        print('额度补偿出错，错误原因：',e)
        db.close()
        return False
    # 关闭数据库
    db.close()
    return True


def rate_fix_56(db, num):
    '''
    将rate_limit中 用户的rate限制增加num条
    '''
    # 获取默认表格
    table = db.table('_default')
    q = Query()

    # 遍历每个记录并检查id是否全部为数字字符,排除给“默认”增加额度的情况
    for record in table.all():
        
        if (record['rate']%10 == 0) or (record['rate']%10 == 1):

            # print("-")
            continue

            # _type = record['type']
            # qq = record['id']
            # new_limit = record['rate'] + num
            # db.upsert({"type": _type, "id": qq, "rate": new_limit}, q.fragment({"type": _type, "id": qq}))
        else:
            print("ori record:", record)
            _type = record['type']
            qq = record['id']
            new_limit = int(record['rate']/10)*10 + 1
            db.upsert({"type": _type, "id": qq, "rate": new_limit}, q.fragment({"type": _type, "id": qq}))
            print("new record:", {"type": _type, "id": qq, "rate": new_limit})
            # print("false")

    # 关闭数据库
    db.close()

def rate_add_num_for_qq(db, num, qq):
    '''
    将rate_limit中,qq用户的rate限制增加num条
    '''
    # 获取默认表格
    table = db.table('_default')
    q = Query()

    find = False

    # 遍历每个记录并检查id是否全部为数字字符,排除给“默认”增加额度的情况
    for record in table.all():

        if ('id' not in record) or (record['id']!=qq):
            continue
        else:
            _type = record['type']
            qq = record['id']
            new_limit = record['rate'] + num

            print(f"为用户{qq}单独添加{num}额度...")
            db.upsert({"type": _type, "id": qq, "rate": new_limit}, q.fragment({"type": _type, "id": qq}))
            print("添加成功")
            find = True
            
    # 关闭数据库
    db.close()
    return find

def date_add_num_for_qq(db, num, qq):
    '''
    将date_start数据库中，所有用户的left增加num天
    '''
    # 获取默认表格
    table = db.table('_default')
    q = Query()
    find = False
    # 遍历每个记录并检查id是否全部为数字字符,排除给“默认”增加额度的情况
    for record in table.all():
        if ('id' in record) and (record['id']==qq):
            find = True
            date = record['date']
            qq = record['id']
            ori_left =  record['left']
            print(f"为用户{qq}单独添加{num}天数...")
            db.upsert({"id": qq, "date":date ,"left": ori_left+num}, q.fragment({"id": qq, "date": date}))
            print("添加成功")
            break
    # 关闭数据库
    db.close()

    return find

def date_add_num(db, num):
    '''
    将date_start数据库中，所有用户的left增加num天
    '''
    # 获取默认表格
    table = db.table('_default')
    q = Query()

    # 遍历每个记录并检查id是否全部为数字字符,排除给“默认”增加额度的情况
    try:
        for record in table.all():
            print("date_add_num天数补偿了用户:", record)
            if 'id' in record and str(record['id']).isdigit():
                date = record['date']
                qq = record['id']
                ori_left =  record['left']
                # print("true")
                db.upsert({"id": qq, "left": ori_left+num}, q.fragment({"id": qq, "date": date}))
            else:
                print("*")
    except Exception as e:
        print('天数补偿出错，错误原因：',e)
        db.close()
        return False
    # 关闭数据库
    db.close()
    return True

def date_change(db, new_left):
    '''
    将date_start数据库中，所有用户的left更新为new_left
    '''
    # 获取默认表格
    table = db.table('_default')
    q = Query()

    # 遍历每个记录并检查id是否全部为数字字符
    for record in table.all():
        print("record:", record)
        if 'id' in record and str(record['id']).isdigit():
            date = record['date']
            qq = record['id']
            # date_list = ["2023-10-25", "2023-10-26", "2023-10-27", "2023-10-28","2023-10-29","2023-10-30","2023-10-31","2023-11-01","2023-11-02","2023-11-03","2023-10-04"]
            # if date in date_list:
            print("true")
            db.upsert({"id": qq, "left": new_left}, q.fragment({"id": qq, "date": date}))
        else:
            print("*")

    # 关闭数据库
    db.close()

def rate_update(limit_db, usage_db, qq, ratetype, _type = "\u597d\u53cb"):
    '''
    qq用户，rate变成ratetype，usage清0
    '''
    q = Query()

    limit = limit_db.get(q.fragment({"type": _type, "id": qq}))
    usage = usage_db.get(q.fragment({"type": _type, "id": qq}))

    # limit 更新
    print("1")
    if limit is None:
        limit = {'type': _type, 'id': qq, 'rate': ratetype}
        limit_db.insert(limit)
    else:
        # 这里的修改使得用户可以一个月内购买多次月卡。
        # 之后在verify更前面的地方判断剩余天数，如果剩太多就不让买。
        # 1108更新：还是覆盖吧，防止主动发消息之类的判断出错
        ori_rate = limit["rate"]
        limit_db.upsert({"type": _type, "id": qq, "rate": ratetype}, q.fragment({"type": _type, "id": qq}))
    # usage 清0
    print("1")
    if usage is None:
        usage = {"type": _type, "id": qq, "count": 0, "time": 0}
        usage_db.insert(usage)
    else:
        usage_db.upsert({"type": _type, "id": qq, "count": 0, "time": 0}, q.fragment({"type": _type, "id": qq}))
    
    limit_db.close()
    usage_db.close()

def overdue_credit_set_zero(date_db, limit_db, tiyan=0):
    '''
    过期额度置为tiyan
    '''
    # 获取默认表格
    table = date_db.table('_default')
    q = Query()
    _type = "\u597d\u53cb"


    for record in table.all():
        
        qq = record['id']

        yueka_days = record['left']
        res_day = yueka_days - Calculate_date(record['date'])
        if res_day<=0:
            # edu清零
            print("record:", record)
            limit_db.upsert({"type": _type, "id": qq, "rate": tiyan}, q.fragment({"type": _type, "id": qq}))
        else:
            print("-")

    # 关闭数据库
    date_db.close()
    limit_db.close()
    
def reset20(db):

    '''
    所有用户的usage减20，或者变为0（使用条数小于20的情况下）
    '''
    # db.update(({"count": re}))

    # 获取默认表格
    table = db.table('_default')
    q = Query()

    # 遍历每个记录并检查id是否全部为数字字符,排除给“默认”增加额度的情况
    for record in table.all():
        

        if record['count']>20:
            # "type": "\u597d\u53cb", "id": "647948352", "count": 7, "time": 21
            _type = record['type']
            qq = record['id']
            new_count = record['count']-20
            # tim = record['time']
            db.upsert({"type": _type, "id": qq, "count": new_count, "time":55}, q.fragment({"type": _type, "id": qq}))
        else:
            _type = record['type']
            qq = record['id']
            new_count = 0
            # tim = record['time']
            db.upsert({"type": _type, "id": qq, "count": new_count, "time":55}, q.fragment({"type": _type, "id": qq}))
    print("success!")
    # 关闭数据库
    db.close()

def update_rates_based_on_date(input_file_A, input_file_B, output_file_B, field_date, field_rate, start_date, end_date):
    with open(input_file_A, 'r', encoding='utf-8-sig') as f_A:
        data_A = json.load(f_A)
    
    with open(input_file_B, 'r', encoding='utf-8-sig') as f_B:
        data_B = json.load(f_B)

    # 日期格式
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)

    # 遍历文件A，筛选符合日期条件的用户ID
    matching_ids = []
    for key in data_A["_default"]:
        date_str = data_A["_default"][key][field_date]
        date_obj = datetime.strptime(date_str, date_format)
        if start_date <= date_obj <= end_date:
            matching_ids.append(data_A["_default"][key]["id"])

    # 遍历文件B，更新符合条件的用户的rate
    for key in data_B["_default"]:
        if data_B["_default"][key]["id"] in matching_ids:
            rate = data_B["_default"][key][field_rate]
            if isinstance(rate, int) and 500 <= rate <= 599:
                data_B["_default"][key][field_rate] = 521

    # 写回更新后的数据到输出文件
    with open(output_file_B, 'w',encoding='utf-8-sig') as f_output_B:
        json.dump(data_B, f_output_B, ensure_ascii=False, indent=4)

# 输入和输出文件路径-改这里
# input_file_A = 'C:/gaungye_bot/ChatailoverBot00/chatgpt/data/date_start.json'
# input_file_B = 'C:/gaungye_bot/ChatailoverBot00/chatgpt/data/rate_limit.json'
# output_file_B = 'C:/gaungye_bot/ChatailoverBot00/chatgpt/data/rate_limit.json'

# # 日期字段和额度字段
# field_date = 'date'
# field_rate = 'rate'

# # 日期范围
# start_date = '2024-05-20'
# end_date = '2024-05-23'


# 将Ajson文件合并到Bjson文件
def append_json_data(file_a_path, file_b_path):
    # 改这里——AB文件路径
    # file_a_path = 'C:\gaungye_bot\ChatailoverBot77\chatgpt\data\data_start.json'
    # file_b_path = 'C:\gaungye_bot\ChatailoverBot77\chatgpt\data\date_start.json'
    with open(file_a_path, 'r') as fileA:
        dataA = json.load(fileA)

    with open(file_b_path, 'r') as fileB:
        dataB = json.load(fileB)

    # 假设数据都在"_default"键下
    dataA_default = dataA["_default"]
    dataB_default = dataB["_default"]

    # 获取文件B中的最大键值
    max_key = max(int(key) for key in dataB_default.keys())

    # 将文件A中的数据顺延到文件B中
    for i, (key, value) in enumerate(dataA_default.items(), start=1):
        new_key = str(max_key + i)
        dataB_default[new_key] = value

    # 保存合并后的数据到文件B
    with open(file_b_path, 'w') as fileB:
        json.dump(dataB, fileB, indent=4)

    print("数据合并完成。")




# # 统一补偿日期备用
# date_add_num(date_start_db_55, 3)
# date_add_num(date_start_db_00, 3)
# date_add_num(date_start_db_66, 2)
# date_add_num(date_start_db_77, 1)
# date_add_num(date_start_db_11, 7)

# rate_add_num(limit_db_55, 20)
# rate_add_num(limit_db_66, 10)
# rate_add_num(limit_db_77, 10)
# rate_add_num(limit_db_11, 10)
# rate_add_num(limit_db_00, 20)


# rate_update(limit_db_55, usage_db_55,1832292582, 601, _type = "\u597d\u53cb")

# rate_add_num_for_qq(limit_db_55, 20, "1832292582")

# reset20(usage_db_00)
# reset20(usage_db_66)
# reset20(usage_db_77)
# reset20(usage_db_55)
# reset20(usage_db_11)

# rate_fix_56(limit_db_55, 5)
# rate_fix_56(limit_db_66, 5)
# rate_fix_56(limit_db_77, 5)
# rate_fix_56(limit_db_11, 5)
# rate_fix_56(limit_db_00, 5)

# overdue_credit_set_zero(date_start_db_00, limit_db_00, 0)
# overdue_credit_set_zero(date_start_db_66, limit_db_66, 0)
# overdue_credit_set_zero(date_start_db_11, limit_db_11, 0)
# overdue_credit_set_zero(date_start_db_55, limit_db_55, 0)
# overdue_credit_set_zero(date_start_db_77, limit_db_77, 0)


# append_json_data('fileA.json', 'fileB.json')
# update_rates_based_on_date(input_file_A, input_file_B, output_file_B, field_date, field_rate, start_date, end_date)
