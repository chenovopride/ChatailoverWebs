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
import os
from datetime import datetime
from loguru import logger

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

# 设置日志（2024/11/22改动）
def setup_logging():
    # 获取当前年月和日期
    current_month = datetime.now().strftime("%Y-%m")
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 每个月一个文件夹
    log_dir = os.path.join("logs", current_month)
    os.makedirs(log_dir, exist_ok=True)

    # 每天一个文件
    log_file = os.path.join(log_dir, f"{current_date}.log")

    # 配置 loguru 日志
    logger.remove()  # 移除默认日志配置
    logger.add(
        log_file,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}",
        rotation="00:00",  # 每天午夜自动创建新日志文件
        retention="30 days",  # 保留 30 天的日志
        compression="zip",  # 压缩旧日志
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

#为每个操作保留登录用户名（2024/11/22改动）
if "username" not in st.session_state:
    st.session_state.username=""

# 登录页面
if st.session_state["logged_in"] == False:
    st.title("登录")
    #username = st.text_input("用户名")
    #记录用户名操作（2024/11/22改动）
    username = st.session_state.username = st.text_input("用户名",value=st.session_state.username) 
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        if login(username, password):
            # print(f'管理员登陆中，用户名：{username}，密码：{password}')
            logging.info(f'管理员登陆中，用户名：{username}，密码：{password}，登录成功~🤭')
            logger.info(f"管理员【{username}】上线！登陆成功！！密码为 {password}~🤭")#登录成功日志（2024/11/22改动）
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            # print('用户名或密码错误')
            logging.info(f'管理员登陆中，用户名：{username}，密码：{password}，登录失败！😕')
            logger.warning(f"管理员【{username}】登录失败!!!😕")#登录失败日志（2024/11/22改动）
            st.error("用户名或密码错误")
            
else:
    st.title('后台管理补偿网站')
    st.write('目前的数据库后端是：', BACKEND)
    st.header('用户补偿')
    user_id = 'all'
    username = st.session_state.username #传入登录页面的用户参数（2024/11/22改动）
    genre = st.radio("补偿某个特定用户还是某个男主的所有用户？",
                        ["所有用户", "特定用户"],
                        captions = ["请在下面选择男主", "请在下面选择男主，并输入用户qq"])
    if genre == "特定用户":
        user_id = st.text_input('用户qq')

    option = st.selectbox("选择男主",("00", "11", "55", "66", "77", "qy", "ls", "sxh", "qc", "xyz", "lzy"))
    days_all = st.number_input('天数',step =1)
    amount_all = st.number_input('额度(必须为10的倍数)',step =10)
    if st.button('提交用户补偿'):
        try:
            logging.info(f'管理员提交用户补偿：{user_id}')
            logger.info(f"管理员【{username}】为【{user_id}】用户的【{option}】男主补偿了【{days_all}】天，【{amount_all}】额度")#记录管理员操作（2024/11/22改动）
            if amount_all %10 == 0:
                modified = compensate(option, user_id, days_all, int(amount_all), backend = BACKEND)
                if modified:
                    st.info(f'补偿成功!')
                    logging.info(f'管理员提交用户补偿：{user_id}成功')
                    logger.info(f'管理员【{username}】为【{user_id}】用户补偿额度成功！！！')#补偿成功提示（2024/11/22改动）
                else:
                    if user_id == 'all':
                        st.error(f'系统并发问题，tinydb容易补偿失败，请联系开发补偿',icon = '❗️')
                    else:
                        st.error(f'没有找到此用户信息，如果用户存在，请再试一次',icon = '❗️')
                    logging.info(f'管理员提交用户补偿：{user_id}成功')
                    logger.info(f'管理员【{username}】为【{user_id}】用户补偿额度成功！！！')#补偿成功提示（2024/11/22改动）
            else:
                st.error(f'补偿失败，额度必须为10的倍数。请重新填写',icon = '❗️')
                logger.exception(f'补偿失败，额度必须为10的倍数!!!')#补偿失败提示（2024/11/22改动）
        except Exception as e:#其他错误（2024/11/22改动）
            error_message=f"补偿失败（未知错误）：{str(e)}"
            logger.exception(f'{error_message}')

    st.header('开关用户功能权限')
    user_id_fun = 'all'
    genre = st.radio("开关某个特定用户还是某个男主的所有用户？",
                        ["所有用户", "特定用户"],
                        captions = ["请在下面选择男主", "请在下面选择男主，并输入用户qq"])
    if genre == "特定用户":
        #user_id_fun = st.text_input('用户qq')
        user_id_fun = st.text_input('用户qq',key="user_function_input")#解决unique key的问题（2024/11/22改动）
    close_flage = st.radio("打开还是关闭？",["打开=1", "关闭=0"])

    option_2 = st.selectbox("选择男主数据库",("00", "11", "55", "66", "77", "qy", "ls", "sxh", "qc", "xyz", "lzy"))
    fuction_name = st.selectbox("选择您要打开或者关闭的功能",("auto_message", "custom_identity", "custom_action", "voice", 
                                                 "sing", "meme", "img_rec", "custom_sched", "menstrual", "custom_sleep",
                                                 "auto_weather", "group", "game", "custom"))

    if st.button('开关用户功能'):
        try:
            logging.info(f'管理员开关用户功能：{user_id}')
            logger.info(f'管理员【{username}】为【{user_id_fun}】用户【{close_flage}】了【{option_2}】的【{fuction_name}】功能')#功能操作日志（2024/11/22改动）
            status = compensate_function(option_2, user_id_fun, fuction_name, int(close_flage[-1]))
            if status:
                st.info(f'补偿成功!')
                logging.info(f'管理员提交用户补偿：{user_id_fun}成功')
                logger.info(f'成功操作！！')#提示成功操作（2024/11/22改动）
            else:
                if user_id_fun == 'all':
                    st.error(f'系统并发问题，请联系开发补偿',icon = '❗️')
                else:
                    st.error(f'没有找到此用户信息，如果用户存在，请再试一次',icon = '❗️')
                logging.info(f'管理员提交用户补偿：{user_id}成功')
                logger.info(f'成功操作！！')#提示成功操作（2024/11/22改动）
        except Exception as e:#其他错误（2024/11/22改动）
            error_message=f"操作失败（未知错误）：{str(e)}"
            logger.exception(f'{error_message}')

    
    st.header('节假日重置20体验额度')
    st.write('未购买用户重置20体验额度(当前无法为未购买用户重置天数), 购买的用户赠送20体验额度。')
    st.write('tinydb后端等待时间较久，而且容易错误，如果出错，联系开发重置即可')
    master_name_reset = st.selectbox("选择游戏",("光夜", "深空", "恋与"))
    # gift_limit = st.number_input('赠送额度(必须为10的倍数)', min_value=0)
    gift_limit = 20
    if st.button('提交重置'):
        modified_count = reset_holiday(master_name_reset, gift_limit_count = gift_limit, backend = BACKEND)
        if modified_count:
            st.info(f'成功!')
            logger.info(f"管理员【{username}】为【{master_name_reset}】提交重置成功！！！")#提交重置成功提示（2024/11/22改动）
        else:
            st.error(f'失败了，请联系开发查看',icon = '❗️')
            logger.info(f"管理员【{username}】为【{master_name_reset}】提交重置【失败】！！！")#提交重置失败提示（2024/11/22改动）
    
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
        logger.info(f'管理员【{username}】已退出登录！')
        st.rerun()

if __name__ == "__main__":
    setup_logging()  # 初始化日志