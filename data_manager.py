"""数据存储模块：把成绩保存到 CSV 文件，并在需要时读回来。"""

import csv
import os
from datetime import datetime

# 相对路径以运行程序时的工作目录为基准，建议在 arduino 目录启动。
FILE = "records.csv"


def save_record(value):
    """追加一条成绩，value 的单位是毫秒。"""
    file_exists = os.path.exists(FILE)
    # "a" 表示追加，不会覆盖已有成绩。
    # newline="" 让 csv 模块处理换行，避免 Windows 下出现多余空行。
    # with 会在代码块结束时自动关闭文件。
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            # 新建文件时先写表头，读取时会通过这些列名取值。
            writer.writerow(["Time", "Reaction(ms)"])
        writer.writerow([datetime.now(), value])


def load_records():
    """返回成绩整数列表；这里只读取反应时间，不返回记录日期。"""
    records = []
    if not os.path.exists(FILE):
        # 第一次运行还没有文件，返回空列表即可。
        return records

    with open(FILE, "r") as f:
        # DictReader 把每行转换为字典，键来自 CSV 的第一行表头。
        reader = csv.DictReader(f)
        for row in reader:
            # CSV 读出的值是字符串，转换为整数后才能进行统计运算。
            records.append(int(row["Reaction(ms)"]))
    return records
