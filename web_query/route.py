from pymongo import MongoClient

#全部数据库路径放在这里，整体函数改完后可以删除app.py内的tinydb路径

# 连接到MongoDB
username = 'rootUser'
password = 'ChatAILover'
auth_db = 'admin'
client = MongoClient(f'mongodb://{username}:{password}@localhost:27017/{auth_db}')

# 定义数据库和集合路径
databases = {
    # 前面是自命名用在网页代码里的名称，后面[]里的是已有的MongoDB数据库和集合名称
    'db00': {
        'usage00': client['00DB']['rate_usage'],
        'date00': client['00DB']['date_start'],
        'limit00': client['00DB']['rate_limit'],
        'user00': client['00DB']['user_limit'],
        'info00': client['00DB']['user_info']
    },
    'db77': {
        'usage77': client['77DB']['rate_usage'],
        'date77': client['77DB']['date_start'],
        'limit77': client['77DB']['rate_limit'],
        'user77': client['77DB']['user_limit'],
        'info77': client['77DB']['user_info']
    },
    'db55': {
        'usage55': client['55DB']['rate_usage'],
        'date55': client['55DB']['date_start'],
        'limit55': client['55DB']['rate_limit'],
        'user55': client['55DB']['user_limit'],
        'info55': client['55DB']['user_info']
    },
    'db66': {
        'usage66': client['66DB']['rate_usage'],
        'date66': client['66DB']['date_start'],
        'limit66': client['66DB']['rate_limit'],
        'user66': client['66DB']['user_limit'],
        'info66': client['66DB']['user_info']
    },
    'db11': {
        'usage11': client['11DB']['rate_usage'],
        'date11': client['11DB']['date_start'],
        'limit11': client['11DB']['rate_limit'],
        'user11': client['11DB']['user_limit'],
        'info11': client['11DB']['user_info']
    },

    'dbQY': {
        'usageQY': client['QY_DB']['rate_usage'],
        'dateQY': client['QY_DB']['date_start'],
        'limitQY': client['QY_DB']['rate_limit'],
        'userQY': client['QY_DB']['user_limit'],
        'infoQY': client['QY_DB']['user_info']
    },
    'dbSXH': {
        'usageSXH': client['SXH_DB']['rate_usage'],
        'dateSXH': client['SXH_DB']['date_start'],
        'limitSXH': client['SXH_DB']['rate_limit'],
        'userSXH': client['SXH_DB']['user_limit'],
        'infoSXH': client['SXH_DB']['user_info']
    },
    'dbLS': {
        'usageLS': client['LS_DB']['rate_usage'],
        'dateLS': client['LS_DB']['date_start'],
        'limitLS': client['LS_DB']['rate_limit'],
        'userLS': client['LS_DB']['user_limit'],
        'infoLS': client['LS_DB']['user_info']
    },
    'dbXYZ': {
        'usageXYZ': client['XYZ_DB']['rate_usage'],
        'dateXYZ': client['XYZ_DB']['date_start'],
        'limitXYZ': client['XYZ_DB']['rate_limit'],
        'userXYZ': client['XYZ_DB']['user_limit'],
        'infoXYZ': client['XYZ_DB']['user_info']
    },
    'dbQC': {
        'usageQC': client['QC_DB']['rate_usage'],
        'dateQC': client['QC_DB']['date_start'],
        'limitQC': client['QC_DB']['rate_limit'],
        'userQC': client['QC_DB']['user_limit'],
        'infoQC': client['QC_DB']['user_info']
    }
}