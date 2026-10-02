"""成绩统计：输入毫秒数列表，返回平均值、最小值或最大值。

文件名与 Python 标准库 statistics 同名；本项目使用的是这个本地模块。
"""


def average(records):
    """平均反应时间 = 全部成绩之和 / 成绩数量。"""
    # 空列表没有平均值，这里约定返回 0，同时避免除以零。
    if len(records) == 0:
        return 0
    return sum(records) / len(records)


def best(records):
    """反应时间越短越好，因此最快成绩取最小值。"""
    if len(records) == 0:
        return 0
    return min(records)


def worst(records):
    """最慢成绩取最大值。"""
    if len(records) == 0:
        return 0
    return max(records)
