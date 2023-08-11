<div align="center">
<article style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
    <p align="center"><img width="300" src="https://user-images.githubusercontent.com/25022954/209616423-9ab056be-5d62-4eeb-b91d-3b20f64cfcf8.svg" /></p>
    <h1 style="width: 100%; text-align: center;"></h1>
</article>
</div>


# 图文数据集下载脚本

> 数据集下载请到：https://opendatalab.com/  （OpenDataLab 是有影响力的数据开源开放平台，公开数据集触手可及。）
---
### 注意事项
>* 请务必使用上述提到的metadata下载地址 然后使用此脚本下载
>* 脚本可以单机或者分布式高速下载处理

---
### 设备及工作环境准备
>* ubuntu服务器
>* python3
>* redis  # 这里默认ip为192.168.0.1 端口为6379
---
### 脚本运行
    # 队列添加任务metadata在哪台机器只在此机器运行一个就行 
    python3 add_task.py
    # monitor_disk.py 每个下载机器开启一个程序
    python monitor_disk.py
    # 开启10个下载进程
    for i in {0..10}; do echo "nohup python3 downloader.py $i >/dev/null 2>&1 &" | bash; done
    # save_error_task.py 把错误队列数据以文本形式保存到本地 根据需要是否开启
    python3 save_error_task.py
    # 下载情况查看
    python3 speed.py
---
### 配置文件说明 setting.py
    # redis连接配置
    redis_ip = "192.168.0.1"
    redis_port = 6379
    redis_db = 0
    redis_pass = "****123***"
    
    dataset_name = "***"
    
    # 使用到的 redis key 配置信息
    class RedisKey:
        task_key = f"{dataset_name}_task"                 # 存放任务队列
        tongji_all = f"{dataset_name}_tongji_all"         # 统计已经加入了多少
        error_key = f"{dataset_name}_task_error"          # 下载失败的任务队列
        tongji_error = f"{dataset_name}_tongji_error"     # 统计下载失败数
        tongji_succ = f"{dataset_name}_tongji_succ"       # 统计下载完成数
        tongji_disk = "tongji_worker_disk"        # 监控磁盘使用量
    
    
    # metadata 目录配置 add_task.py 使用  样例：/mnt/vdb/***/metadata/url1.txt； /mnt/vdb/***/metadata/url2.txt； /mnt/vdb/***/metadata/url3.txt
    metadata_dir = f"/mnt/vdb/{dataset_name}/metadata"
    # 添加任务时候队列中少于5000000 开始执行添加任务
    addtask_threshold = 5000000
    # 添加过后的metadata路径写入 done_part.txt
    done_path = "./done_part.txt"
    
    
    # monitor_disk.py  查看存储空间占用情况
    monitor_disk = '/mnt/vdc'
    
    
    # downloader.py  下载的图片存储的目录 后续会拼接 laion1B-nolang  laion1B-nolang 等目录
    store_dir = f"/mnt/vdc/{dataset_name}/data/"
    # 这里设置磁盘使用阈值是5000 GB   单位：GB
    stop_threshold = 5000
    # 下载多线程数 默认：32
    thread_num = 32
    
    # save_error_task.py  本地持久化redis错误队列数据 根据需要是否持久化 一般要开启此程序 否则错误较多redis占用较高
    store_error_dir = "./error_task/"

