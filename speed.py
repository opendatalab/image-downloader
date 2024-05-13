# -*- coding:utf-8 -*-
# @Time: 2022/12/21 23:42
# @Author: willian
# @File：speed.py
# @desc:

import time
import redis
import setting

from setting import RedisKey

redis_client = redis.Redis(host=setting.redis_ip, port=setting.redis_port, db=setting.redis_db, password=setting.redis_pass, encoding="utf-8", decode_responses=True)


def get_count(r_key):
    count_num = redis_client.get(r_key)
    if count_num:
        return int(count_num)
    else:
        # 初始化情况下没有此redis的key 获取为None 
        return 0

def speed():
    error = RedisKey.tongji_error
    succ = RedisKey.tongji_succ
    while True:
        s_c = get_count(error) + get_count(succ)
        time.sleep(10)
        e_c = get_count(error) + get_count(succ)
        c = e_c-s_c
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}   10秒钟处理：{c}  处理速率：{c/10}")


if __name__ == '__main__':
    speed()
