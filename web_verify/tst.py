import time
from tinydb import TinyDB, Query
from tinydb.operations import increment
from tinydb.table import Document
import datetime
from app import * 
from permission import *

limit_db_55 = TinyDB(r"C:\Windows-quickstart-go-cqhttp-refs.tags.55bot\chatgpt\data\rate_limit.json")

# mon_card_remain_days(date_start_db_55, "18392440042")
_type = "\u597d\u53cb"
# wending_rate_55 = 600



rate_update(limit_db_55,usage_db_55, "1832292582", 601, _type)
date_update(date_start_db_55, "1832292582")