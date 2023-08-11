# -*- coding:utf-8 -*-
# @Time: 2023/8/11 12:54
# @Author: willian
# @File：add_task_txt.py
# @desc:

import os
import json
import time
import redis
import hashlib
import setting as se

from loguru import logger

from setting import RedisKey

logger_format = "{time:YYYY-MM-DD HH:mm:ss,SSS} [{thread}] {level} {file} {line} - {message}"

redis_client = redis.Redis(host=se.redis_ip, port=se.redis_port, db=se.redis_db, password=se.redis_pass, encoding="utf-8", decode_responses=True)
task_key = RedisKey.task_key
tongji_all = RedisKey.tongji_all


def sha256(text):
    h = hashlib.sha256(str(text).encode())
    return h.hexdigest()


def add_task():
    logger.add("./logs/add_task/add_task_{time:YYYY-MM-DD}.log", format=logger_format, level="INFO", rotation="00:00",
               retention='60 days')
    part_done = set()
    done_path = se.done_path
    if os.path.exists(done_path):
        with open(done_path, "rb") as f:
            for line in f:
                if line:
                    part_done.add(line.strip().decode())
    while True:
        if redis_client.llen(task_key) > se.addtask_threshold:
            time.sleep(10*60)
            continue
        filename = ""
        base_path = se.parquet_dir
        for file_name in os.listdir(base_path):
            full_path = f"{base_path}/{file_name}"
            if full_path not in part_done:
                filename = full_path
                break
        # print(filename)
        if filename == "":
            break

        logger.info(f"开始添加task任务，   part_file: {filename}")
        i = 0
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                i += 1
                img_url = line.strip()
                image_id = sha256(img_url)
                img_path = f"/{se.dataset_name}/images/{image_id}.jpg"
                task_json = {"img_path": img_path, "img_url": img_url}
                logger.debug(f"添加任务：{task_json}")
                task_str = json.dumps(task_json)
                redis_client.lpush(task_key, task_str)
        logger.info(f"任务添加完成， task数：{i}   part_file: {filename}")

        with open(done_path, "ab+") as f:
            f.write(filename.encode())
            f.write(b"\n")
        part_done.add(filename)


if __name__ == '__main__':
    add_task()