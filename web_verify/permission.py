import time
from tinydb import TinyDB, Query
from tinydb.operations import increment
from tinydb.table import Document
import datetime

def rate_add_edu(usage_db, date_start_db, limit_db, qq,_type, edu):
    q = Query()
    limit = limit_db.get(q.fragment({"type": _type, "id": qq}))
    if limit is None:
        limit = {'type': _type, 'id': qq, 'rate': edu}
        limit_db.insert(limit)
        print("用户没买月卡直接买的额度，qq:",qq)
        date_update(date_start_db, qq)
        # 0127:cyx:发现单独买额度的用户如果直接查询还是查不到，遂添加
        usage = {"type": _type, "id": qq, "count": 0, "time": 0}
        usage_db.insert(usage)
    else:
        ori_rate = limit["rate"]
        limit_db.upsert({"type": _type, "id": qq, "rate": ori_rate+edu}, q.fragment({"type": _type, "id": qq}))
        print("用户:",qq, "单买额度添加成功！")

# usage不清0的额度叠加，和rate_add_edu的区别是rate_add_edu可以解决用户没卡，要为他新建卡的情况。
# rate_add_edu_with_card必须是确定有卡(天数)，但是不确定有没有limit 和 usage
def rate_add_edu_with_card(limit_db, usage_db, qq, ratetype, _type):
    q = Query()
    limit = limit_db.get(q.fragment({"type": _type, "id": qq}))
    usage = usage_db.get(q.fragment({"type": _type, "id": qq}))

    # limit 更新
    if limit is None:
        limit = {'type': _type, 'id': qq, 'rate': ratetype}
        try:
            limit_db.insert(limit)
        except Exception as e:
            yichang_str = str(e)
            print("异常存在于limit_db.insert, 异常为：", yichang_str)
    else:
        ori_rate = limit["rate"]
        try:
            # 额度叠加
            limit_db.upsert({"type": _type, "id": qq, "rate": ori_rate+ratetype}, q.fragment({"type": _type, "id": qq}))
        except Exception as e:
            yichang_str = str(e)
            print("异常存在于limit_db.upsert, 异常为：", yichang_str)
    # usage 不清0，如果这个用户没有usage，说明是新人，给她加上
    if usage is None:
        usage = {"type": _type, "id": qq, "count": 0, "time": 0}
        try:
            usage_db.insert(usage)
        except Exception as e:
            yichang_str = str(e)
            print("异常存在于usage_db.insert, 异常为：", yichang_str)

def rate_update(limit_db, usage_db, qq, ratetype, _type):
    q = Query()
    limit = limit_db.get(q.fragment({"type": _type, "id": qq}))
    usage = usage_db.get(q.fragment({"type": _type, "id": qq}))

    # limit 更新
    if limit is None:
        limit = {'type': _type, 'id': qq, 'rate': ratetype}
        try:
            limit_db.insert(limit)
        except Exception as e:
            yichang_str = str(e)
            print("异常存在于limit_db.insert, 异常为：", yichang_str)
    else:
        # 这里的修改使得用户可以一个月内购买多次月卡。
        # 之后在verify更前面的地方判断剩余天数，如果剩太多就不让买。
        # 1108更新：还是覆盖吧，防止主动发消息之类的判断出错
        ori_rate = limit["rate"]
        try:
            limit_db.upsert({"type": _type, "id": qq, "rate": ratetype}, q.fragment({"type": _type, "id": qq}))
        except Exception as e:
            yichang_str = str(e)
            print("异常存在于limit_db.upsert, 异常为：", yichang_str)
    # usage 清0
    if usage is None:
        usage = {"type": _type, "id": qq, "count": 0, "time": 0}
        try:
            usage_db.insert(usage)
        except Exception as e:
            yichang_str = str(e)
            print("异常存在于usage_db.insert, 异常为：", yichang_str)
    else:
        try:
            usage_db.upsert({"type": _type, "id": qq, "count": 0, "time": 0}, q.fragment({"type": _type, "id": qq}))
        except Exception as e:
            yichang_str = str(e)
            print("异常存在于usage_db.upsert, 异常为：", yichang_str)


def date_update(date_start_db, _id):
    """更新付费日期"""
    Q = Query()
    date = str(datetime.date.today())
    date_and_id = {'id': _id, 'date': date, 'left' : 31}

    if len(date_start_db.search(Q.id == _id)) != 0:
        #计算购买日距离今日有多久
        #购买日距今＞31，则执行逻辑2，购买日距今＜31，即left＞0，执行逻辑1
        # left = 31 -  calculate_date(date) 
        date_data = date_start_db.get(Q.fragment({"id": _id}))
        ori_date_buy = date_data["date"]
        
        left = date_data["left"] - Calculate_date(ori_date_buy)
        if left > 0:
            # 0503更新：用戶月卡一律視爲覆蓋
            add = 31 + left
            date_start_db.upsert({"id": _id,"date":date, "left": 31}, Q.fragment({"id": _id}))
            # date_start_db.update(({"date": date, "left" : add}), (Q.id == _id))
        else:
            date_start_db.upsert({"id": _id,"date":date, "left": 31}, Q.fragment({"id": _id}))
            # date_start_db.update(({"date": date, "left" : 31}), (Q.id == _id))
    else:
        date_start_db.insert(date_and_id)

def jika_date_update(date_start_db, _id):
    """更新付费日期"""
    jika_days = 91
    Q = Query()
    date = str(datetime.date.today())
    date_and_id = {'id': _id, 'date': date, 'left' : jika_days}

    if len(date_start_db.search(Q.id == _id)) != 0:
        #计算购买日距离今日有多久
        date_data = date_start_db.get(Q.fragment({"id": _id}))
        ori_date_buy = date_data["date"]

        left = date_data["left"] - Calculate_date(ori_date_buy)
        if left > 0:
            # 允许多次购买后卡的天数叠加
            add = jika_days + left
            date_start_db.upsert({"id": _id,"date":date, "left": add}, Q.fragment({"id": _id}))
        else:
            date_start_db.upsert({"id": _id,"date":date, "left": jika_days}, Q.fragment({"id": _id}))

    else:
        date_start_db.insert(date_and_id)


def Calculate_date(date):
    date_today = datetime.date.today()
    date_today = str(date_today).split("-")
    date_1 = datetime.date(int(date_today[0]), int(date_today[1]), int(date_today[2]))
    date_buy = str(date).split("-")
    date_2 = datetime.date(int(date_buy[0]), int(date_buy[1]), int(date_buy[2]))
    date_3 = date_1 - date_2
    date_3 = str(date_3).split(" ")
    if date_3[0] == '0:00:00':
        res = 0
    else:
        res = int(date_3[0])
    
    return res

def mon_card_remain_days(data_start_db, qq):
    q = Query()
    usage = data_start_db.get(q.fragment({"id": str(qq)}))
    if usage is None:
        print("qq is invalid or never use.")
        return -1
    else:
        print("remain days:", usage["left"])
        return usage["left"]

class RateLimitManager:
    """额度管理器"""

    def __init__(self):
        self.limit_db = TinyDB("data/rate_limit.json")
        self.usage_db = TinyDB("data/rate_usage.json")
        self.draw_limit_db = TinyDB("data/draw_rate_limit.json")
        self.draw_usage_db = TinyDB("data/draw_rate_usage.json")
        self.per_10 = TinyDB("data/usage_per_10.json")
        self.date_start_db = TinyDB("data/date_start_db.json")

    def update(self, _type: str, _id: str, rate: int):
        """更新额度限制"""

        q = Query()
        self.limit_db.upsert({"type": _type, "id": _id, "rate": rate}, q.fragment({"type": _type, "id": _id}))

    def update_draw(self, _type: str, _id: str, rate: int):
        """更新画图额度限制"""

        q = Query()
        self.draw_limit_db.upsert({"type": _type, "id": _id, "rate": rate}, q.fragment({"type": _type, "id": _id}))

    def update_per_10(self, _type: str, _id: str, rate: int):
        """更新每十分钟使用量限制"""

        q = Query()
        self.per_10.upsert({"type": _type, "id": _id, "rate": rate}, q.fragment({"type": _type, "id": _id}))

    def list(self):
        """列出所有的额度限制"""

        return self.limit_db.all()

    def get_limit(self, _type: str, _id: str) -> Document:
        """获取限制"""

        q = Query()
        entity = self.limit_db.get(q.fragment({"type": _type, "id": _id}))
        if entity is None and _id != '默认':
            return self.limit_db.get(q.fragment({"type": _type, "id": '默认'}))
        return entity

    def get_draw_limit(self, _type: str, _id: str) -> Document:
        """获取画图限制"""

        q = Query()
        entity = self.draw_limit_db.get(q.fragment({"type": _type, "id": _id}))
        if entity is None and _id != '默认':
            return self.draw_limit_db.get(q.fragment({"type": _type, "id": '默认'}))
        return entity

    def get_draw_usage(self, _type: str, _id: str) -> Document:
        """获取画图使用量"""

        q = Query()
        usage = self.draw_usage_db.get(q.fragment({"type": _type, "id": _id}))
        current_time = time.localtime(time.time()).tm_hour

        # 删除过期的记录
        if usage is not None and usage['time'] != current_time:
            self.draw_usage_db.remove(doc_ids=[usage.doc_id])
            usage = None

        # 初始化
        if usage is None:
            usage = {'type': _type, 'id': _id, 'count': 0, 'time': current_time}
            self.draw_usage_db.insert(usage)

        return usage

    def get_usage(self, _type: str, _id: str) -> Document:
        """获取使用量"""

        q = Query()
        usage = self.usage_db.get(q.fragment({"type": _type, "id": _id}))
        current_time = time.localtime(time.time()).tm_hour

        '''# 删除过期的记录
        if usage is not None and usage['time'] != current_time:
            self.usage_db.remove(doc_ids=[usage.doc_id])
            usage = None'''

        # 初始化
        if usage is None:
            usage = {'type': _type, 'id': _id, 'count': 0, 'time': current_time}
            self.usage_db.insert(usage)

        return usage
    
    def get_msgnum(self, _type: str, _id: str) -> Document:
        """获取每十分钟使用量"""

        q = Query()
        usage = self.per_10.get(q.fragment({"type": _type, "id": _id}))
        current_time_m = time.localtime(time.time()).tm_min
        current_time_h = time.localtime(time.time()).tm_hour

        # 删除过期的记录
        if usage is not None and usage['time_h'] != current_time_h:
            self.per_10.remove(doc_ids=[usage.doc_id])
            usage = None
        elif usage is not None and int(usage['time_m']) > int(current_time_m) and int(usage['time_m']) - int(current_time_m) >10:
                self.per_10.remove(doc_ids=[usage.doc_id])
                usage = None
        elif usage is not None and int(usage['time_m']) < int(current_time_m) and (int(usage['time_m']) + 60 - int(current_time_m)) >10:
                    self.per_10.remove(doc_ids=[usage.doc_id])
                    usage = None


        # 初始化
        if usage is None:
            usage = {'type': _type, 'id': _id, 'count': 0, 'time_h': current_time_h, 'time_m' : current_time_h}
            self.per_10.insert(usage)

        return usage
    
    
    def date_update(self, _id):
        """更新付费日期"""
        Q = Query()
        date = str(datetime.date.today())
        date_and_id = {'id': _id, 'date': date, 'left' : 31}
        if len(self.date_start_db.search(Q.id == _id)) != 0:
            left = self.Calculate_date(date_and_id["date"])
            if left > 0:
                add = 31 + left
                self.date_start_db.update(({"date": date, "left" : add}), (Q.id == _id))
            else:
                self.date_start_db.update(({"date": date, "left" : 31}), (Q.id == _id))
        else:
            self.date_start_db.insert(date_and_id)


    def Calculate_date(self, date):
        date_today = datetime.date.today()
        date_today = str(date_today).split("-")
        date_1 = datetime.date(int(date_today[0]), int(date_today[1]), int(date_today[2]))
        date_buy = str(date).split("-")
        date_2 = datetime.date(int(date_buy[0]), int(date_buy[1]), int(date_buy[2]))
        date_3 = date_1 - date_2
        date_3 = str(date_3).split(" ")
        if date_3[0] == '0:00:00':
            res = 0
        else:
            res = int(date_3[0])
        
        return res
        


    def increment_usage(self, _type, _id):
        """更新使用量"""

        self.get_usage(_type, _id)

        q = Query()
        self.usage_db.update(increment('count'), q.fragment({"type": _type, "id": _id}))

    def increment_draw_usage(self, _type, _id):
        """更新画图使用量"""

        self.get_usage(_type, _id)

        q = Query()
        self.draw_usage_db.update(increment('count'), q.fragment({"type": _type, "id": _id}))

    def increment_usage_per_10(self, _type, _id):
        """更新每十分钟使用量"""

        self.get_msgnum(_type, _id)

        q = Query()
        self.per_10.update(increment('count'), q.fragment({"type": _type, "id": _id}))

    def check_exceed(self, _type: str, _id: str) -> float:
        """检查是否超额，返回 使用量/额度"""

        limit = self.get_limit(_type, _id)
        usage = self.get_usage(_type, _id)

        # 此类型下无限制
        if limit is None:
            return 0

        # 此类型下为禁止
        return 1 if limit['rate'] == 0 else usage['count'] / limit['rate']
    
    def check_buy_date(self, _id):
        Q = Query()
        date_buy = self.date_start_db.search(Q.id == _id)
        if len(date_buy) != 0:
            date = date_buy[0]["date"]
            left = date_buy[0]["left"]
            res = self.Calculate_date(date)
            if res < left:
                #使用未到期
                return 0
            else:
                #使用已到期
                return 1
        else:
            #未购买
            return -1

        
