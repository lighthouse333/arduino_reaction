"""桌面程序入口：创建界面、发起测试，并显示历史成绩。

需要安装第三方库 pyserial 和 matplotlib，运行前连接 Arduino。
当前示例使用 COM5；如果电脑分配了其他串口，请修改下面的端口名。
"""

import tkinter as tk
import serial
import threading

from data_manager import save_record, load_records
# 这里导入的是同目录下的 statistics.py，而不是 Python 的同名标准库。
from statistics import average, best, worst
from plot import show_plot


# 串口是电脑与 Arduino 传递命令和结果的通道。
# 9600 是波特率，必须与固件中的 Serial.begin(9600) 一致。
# 当前在启动时连接设备：端口不存在或被占用时，程序会报错。
arduino = serial.Serial("COM5", 9600)


def update_statistics():
    """读取全部成绩，刷新统计数字和最近 10 条历史记录。"""
    records = load_records()
    count_label.config(text=f"测试次数：{len(records)}")

    if len(records) > 0:
        # :.1f 表示保留一位小数；反应时间越短，成绩越好。
        average_label.config(text=f"平均：{average(records):.1f} ms")
        best_label.config(text=f"最快：{best(records)} ms")
        worst_label.config(text=f"最慢：{worst(records)} ms")

    # 先清空列表再重新填入，避免每次刷新都追加重复的记录。
    history.delete(0, tk.END)
    # [-10:] 是列表切片：取最后 10 条，不足 10 条时取全部。
    for r in records[-10:]:
        history.insert(tk.END, f"{r} ms")


def run_tests(rounds):
    """依次完成 rounds 轮测试，每轮收到成绩后才进入下一轮。"""
    for i in range(rounds):
        print(f"第 {i+1} 次测试")

        # b 前缀表示字节数据；串口 write() 接收字节，而不是普通字符串。
        # 换行符是命令结束标记，对应 Arduino 的 readStringUntil('\n')。
        arduino.write(b"START\n")

        while True:
            # readline() 读取到换行符为止；未设置超时，无响应时会一直等待。
            data = arduino.readline()
            # decode() 将字节转为字符串，strip() 去掉两端的换行和空白。
            text = data.decode().strip()
            print(text)

            # 双方约定结果格式为 TIME:393，单位是毫秒。
            if text.startswith("TIME:"):
                value = int(text.split(":")[1])
                save_record(value)

                # 学习提示：此处沿用原实现，在工作线程里更新界面。
                # 更稳妥的做法是用队列配合 window.after()，让主线程更新控件。
                result.config(text=f"成绩：{value} ms")
                print("成绩:", value)
                # break 只退出内层 while，外层 for 仍会继续下一轮。
                break

        update_statistics()


def start_test():
    """读取输入框里的轮数，启动后台测试线程。"""
    try:
        rounds = int(round_entry.get())
    except ValueError:
        # 输入不是整数时使用默认值，例如输入了空字符串或汉字。
        rounds = 5

    # 等待硬件会阻塞线程，放在后台可以让界面继续响应操作。
    # daemon=True 表示主程序退出时，不必等待这个线程结束。
    # 当前未限制重复点击；请等本轮全部结束后再开始，避免线程争抢串口。
    threading.Thread(
        target=run_tests,
        args=(rounds,),  # 单元素元组需要末尾的逗号，用它向函数传参。
        daemon=True,
    ).start()


# Tk() 创建主窗口。下面创建的控件都放在这个窗口里。
window = tk.Tk()
window.title("Arduino Reaction Test")
window.geometry("500x650")

# Label 用于显示文字，pack() 负责按创建顺序排列控件。
# pady 设置上下留白；font 中的数字表示字号。
title = tk.Label(window, text="Reaction Test", font=("Arial", 24))
title.pack(pady=20)

result = tk.Label(window, text="成绩：-- ms", font=("Arial", 18))
result.pack(pady=10)

count_label = tk.Label(window, text="测试次数：0", font=("Arial", 16))
count_label.pack()
average_label = tk.Label(window, text="平均：-- ms", font=("Arial", 16))
average_label.pack()
best_label = tk.Label(window, text="最快：-- ms", font=("Arial", 16))
best_label.pack()
worst_label = tk.Label(window, text="最慢：-- ms", font=("Arial", 16))
worst_label.pack()

history_title = tk.Label(window, text="历史记录", font=("Arial", 16))
history_title.pack(pady=10)
# Listbox 是可逐行添加内容的列表；height=10 表示显示约 10 行。
history = tk.Listbox(window, height=10, width=20)
history.pack()

tk.Label(window, text="测试次数:").pack()
# Entry 是单行输入框，insert(0, ...) 在开头放入默认值。
round_entry = tk.Entry(window)
round_entry.insert(0, "5")
round_entry.pack()

# command 传函数本身，不加括号；点击按钮时才会调用函数。
button = tk.Button(
    window, text="开始测试", font=("Arial", 16), command=start_test
)
button.pack(pady=20)
plot_button = tk.Button(
    window, text="查看曲线", font=("Arial", 16), command=show_plot
)
plot_button.pack(pady=10)

# 控件创建完毕后才能刷新它们；启动时也会载入以前保存的成绩。
update_statistics()
# 进入事件循环，持续处理点击、键盘输入和窗口重绘，直到关闭窗口。
window.mainloop()
