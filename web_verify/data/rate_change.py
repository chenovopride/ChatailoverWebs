from tinydb import TinyDB, Query

def rate_change(db, num):
    # 获取默认表格
    table = db.table('_default')
    q = Query()

    # 遍历每个记录并检查id是否全部为数字字符
    for record in table.all():
        print("record:", record)
        if 'id' in record and str(record['id']).isdigit():
            print("true")

            _type = record['type']
            qq = record['id']
            new_limit = record['rate'] + num

            db.upsert({"type": _type, "id": qq, "rate": new_limit}, q.fragment({"type": _type, "id": qq}))
        else:
            print("false")

    # 关闭数据库
    db.close()

# 读取数据库文件
rate_limit = TinyDB('rate_limit_tst.json')
rate_change(rate_limit, 3)