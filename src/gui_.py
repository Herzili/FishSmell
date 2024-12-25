import tkinter as tk
from tkinter import filedialog
from pull import pull_main
from noise_estb import estb_main
from fuzz_rule import fuzz_rule_main
from atwt import atwt_main
from SGBNR import sgbnr_main
import shared
import os

def choose_file():
    # 打开文件选择对话框，返回文件路径
    shared.isselected = 1
    global file_path
    file_path = filedialog.askopenfilename()
    print(file_path[-3:])
    if file_path[-3:] == 'tif':
        # 更新底部状态信息
        status_label.config(text="源图像已选择，点击处理")
    else :
        print("A")
        exit()

def start_operation():
    if shared.isselected == 0 :
        status_label.config(text="还未选择图像！")
        return
    global file_path
    global outpath
    print(file_path)
    print(outpath)
    img =pull_main(file_path,outpath)
    factor = estb_main(img)
    agr1,*agr2 = fuzz_rule_main(factor)
    img = sgbnr_main(img,outpath,agr2[0],agr2[1],agr2[2],agr2[3],agr2[4])
    shared.循环次数 = 1

# 创建主窗口
file_path = ""
outpath = os.getcwd()
frame = tk.Tk()
frame.title("鱼香肉丝v0.1")
frame.geometry("400x180")
frame.resizable(True, False)  #允许调整窗口大小
# 文件选择按钮
file_button = tk.Button(frame, text="选择文件", command=choose_file,width=40)
file_button.place(x=60, y=20)
# 开始按钮
start_button = tk.Button(frame, text="处理", command=start_operation,width=40)
start_button.place(x=60, y=80)
# 底部状态信息标签
s_label = tk.Label(frame, text="状态:  ")
s_label.place(x=60, y=140)

status_label = tk.Label(frame, text="未开始")
status_label.place(x=110, y=140)

# 运行主循环
frame.mainloop()

