'''
streamlit UI + 逻辑

'''
import streamlit as st
from pymongo import MongoClient
# from backend_mongo import *
# from backend_tinydb import *
from backend_wrapper import *
import sys
import logging

# 这里设置数据库后端
BACKEND = 'mongodb'

# 设置日志记录
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='w', # 每次运行app.py 都会新生成log. 使用‘a’更换为追加模式
    encoding='utf-8'  # 指定编码为 UTF-8
)


# 定义登录验证函数
def login(username, password):
    if password == "asdf":
        return True
    else:
        return False
    
# 初始化Session State
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# 登录页面
if st.session_state["logged_in"] == False:
    st.title("登录")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        if login(username, password):
            # print(f'管理员登陆中，用户名：{username}，密码：{password}')
            logging.info(f'管理员登陆中，用户名：{username}，密码：{password}，登录成功~🤭')
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            # print('用户名或密码错误')
            logging.info(f'管理员登陆中，用户名：{username}，密码：{password}，登录失败！😕')
            st.error("用户名或密码错误")
            
else:
    st.title('后台管理补偿网站')
    st.write('目前的数据库后端是：', BACKEND)
    st.header('用户补偿')
    user_id = 'all'
    genre = st.radio("补偿某个特定用户还是某个男主的所有用户？",
                        ["所有用户", "特定用户"],
                        captions = ["请在下面选择男主", "请在下面选择男主，并输入用户qq"])
    if genre == "特定用户":
        user_id = st.text_input('用户qq')

    option = st.selectbox("选择男主",("00", "11", "55", "66", "77", "qy", "ls", "sxh", "qc", "xyz"))
    days_all = st.number_input('天数',step =1)
    amount_all = st.number_input('额度(必须为10的倍数)',step =10)
    if st.button('提交用户补偿'):
        logging.info(f'管理员提交用户补偿：{user_id}')
        if amount_all %10 == 0:
            modified = compensate(option, user_id, days_all, int(amount_all), backend = BACKEND)
            if modified:
                st.info(f'补偿成功!')
                logging.info(f'管理员提交用户补偿：{user_id}成功')
            else:
                if user_id == 'all':
                    st.error(f'系统并发问题，tinydb容易补偿失败，请联系开发补偿',icon = '❗️')
                else:
                    st.error(f'没有找到此用户信息，如果用户存在，请再试一次',icon = '❗️')
                logging.info(f'管理员提交用户补偿：{user_id}成功')
        else:
            st.error(f'补偿失败，额度必须为10的倍数。请重新填写',icon = '❗️')

    st.header('开关用户功能权限')
    user_id_fun = 'all'
    genre = st.radio("开关某个特定用户还是某个男主的所有用户？",
                        ["所有用户", "特定用户"],
                        captions = ["请在下面选择男主", "请在下面选择男主，并输入用户qq"])
    if genre == "特定用户":
        user_id_fun = st.text_input('用户qq')
    close_flage = st.radio("打开还是关闭？",["打开=1", "关闭=0"])

    option_2 = st.selectbox("选择男主数据库",("00", "11", "55", "66", "77", "qy", "ls", "sxh", "qc", "xyz"))
    fuction_name = st.selectbox("选择您要打开或者关闭的功能",("auto_message", "custom_identity", "custom_action", "voice", 
                                                 "sing", "meme", "img_rec", "custom_sched", "menstrual", "custom_sleep",
                                                 "auto_weather", "group", "game", "custom"))

    if st.button('开关用户功能'):
        logging.info(f'管理员开关用户功能：{user_id}')
        status = compensate_function(option_2, user_id_fun, fuction_name, int(close_flage[-1]))
        if status:
            st.info(f'补偿成功!')
            logging.info(f'管理员提交用户补偿：{user_id_fun}成功')
        else:
            if user_id_fun == 'all':
                st.error(f'系统并发问题，请联系开发补偿',icon = '❗️')
            else:
                st.error(f'没有找到此用户信息，如果用户存在，请再试一次',icon = '❗️')
            logging.info(f'管理员提交用户补偿：{user_id}成功')

    
    st.header('节假日重置20体验额度')
    st.write('未购买用户重置20体验额度, 购买的用户赠送20体验额度。')
    st.write('tinydb后端等待时间较久，而且容易错误，如果出错，联系开发重置即可')
    master_name_reset = st.selectbox("选择游戏",("光夜", "深空(请勿使用)"))
    # gift_limit = st.number_input('赠送额度(必须为10的倍数)', min_value=0)
    gift_limit = 20
    if st.button('提交重置'):
        modified_count = reset_holiday(master_name_reset, gift_limit_count = gift_limit, backend = BACKEND)
        if modified_count:
                st.info(f'成功!')
        else:
            st.error(f'失败了，请联系开发查看',icon = '❗️')
    
    # st.header('查看用户自定义情况')
    # master_name_info = st.text_input('男主名 (用户信息)')
    # user_info_id = st.text_input('用户ID (用户信息)')
    # if st.button('查看用户自定义情况'):
    #     user_info = get_user_info(master_name_info, user_info_id)
    #     st.info(user_info)

    # st.header('查看用户购买功能情况')
    # master_name_limit = st.text_input('男主名 (用户购买功能)')
    # user_limit_id = st.text_input('用户ID (用户购买功能)')
    # if st.button('查看用户购买功能'):
    #     user_limit = get_user_limit(master_name_limit, user_limit_id)
    #     st.info(user_limit)

    # st.header('设置功能')
    # master_name_active = st.text_input('男主名 (主动版)')
    # user_active_id = st.text_input('用户ID (主动版)')
    # if st.button('设置为主动版'):
    #     modified_count = set_active(master_name_active, user_active_id)
    #     st.info(f'设置为主动版成功，共修改了 {modified_count} 个用户')

    # master_name_custom = st.text_input('男主名 (定制版)')
    # user_custom_id = st.text_input('用户ID (定制版)')
    # if st.button('设置为定制版'):
    #     modified_count = set_custom(master_name_custom, user_custom_id)
    #     st.info(f'设置为定制版成功，共修改了 {modified_count} 个用户')

    st.header('券码查找（还未上线请勿使用）')
    coupon_code = st.text_input('券码')
    # if st.button('查找用户QQ'):
    #     user = find_coupon_user(coupon_code)
    #     st.info(user)
    

    
    if st.button('退出登录', type="primary"):
        st.session_state["logged_in"] = False
        st.rerun()