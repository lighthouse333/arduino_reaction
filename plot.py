"""绘图模块：读取历史成绩，用折线图展示每次测试的反应时间。"""

import matplotlib.pyplot as plt
from data_manager import load_records


def show_plot():
    """打开图表窗口；横轴为历史测试序号，纵轴为毫秒数。"""
    records = load_records()
    if len(records) == 0:
        print("No data")
        return

    # range 的结束值不包含在内，故加 1，生成 1 到成绩数量的序号。
    rounds = range(1, len(records) + 1)
    # figsize 的单位是英寸；每次调用都新建一张图。
    plt.figure(figsize=(8, 4))
    plt.plot(rounds, records, marker="o")  # 圆点标出每一次测试。
    plt.title("Reaction Time Trend")
    plt.xlabel("Round")
    plt.ylabel("Reaction Time(ms)")
    plt.grid(True)  # 网格便于对照坐标轴读取数值。
    plt.show()


# 直接运行本文件会显示曲线；被 main.py 导入时不会执行这里。
if __name__ == "__main__":
    show_plot()
