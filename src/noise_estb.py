from skimage import io,color
import numpy as np
import random
import shared

#传入拉伸之后的图片
def  hsv_var(block):
    """
    计算给定区块的三个通道的方差和明度平均值
    """
    # 将RGB区块转换为HSV
    hsv_block = color.rgb2hsv(block)
    # 获取饱和度通道（S）和明度通道（V）
    hue = hsv_block[:, :, 0]
    saturation = hsv_block[:, :, 1]
    luminance = hsv_block[:, :, 2]
    # 计算方差和亮度平均值
    hue_var = np.var(hue)
    saturation_var = np.var(saturation)
    luminance_var = np.var(luminance)
    luminance_mean = np.mean(luminance)
    return hue_var,saturation_var, luminance_var,luminance_mean

'''#色调方差，饱和度方差，明度方差
    return filtered_vars[index,0],filtered_vars[index,1],filtered_vars[index,2]'''
def estb_main(img):
    print("评估噪声水平...")
    shared.log = "评估噪声水平..."
    image = img
    # 获取图像的高度和宽度
    height, width = image.shape[0], image.shape[1]
    # 设置区块的大小
    block_size = 40
    # 选取 30 个区块
    num_blocks = 30
    # 存储区块的列表
    blocks_list = []

    #判断存储类型
    归一化数值 = -1
    if image.max() <=1:     #浮点
        归一化数值 = 1
    elif image.max() >150 and image.max() <256: #8bit整形
        归一化数值 = 255
    elif image.max() >40000 and image.max() <65536: #16bit整形
        归一化数值 = 65535
    else:
        print('格式不支持！检查位深和浮整')
        exit()
    print("归一化数值是",归一化数值)
    image = image / 归一化数值

    for _ in range(num_blocks):
        start_row = random.randint(0, height - block_size)
        start_col = random.randint(0, width - block_size)
        block = image[start_row:start_row + block_size, start_col:start_col + block_size]
        blocks_list.append(block)

    #存储方差数据
    vars = np.zeros((num_blocks,4)) 
    for i in range(num_blocks):
            vars[i,0],vars[i,1],vars[i,2],vars[i,3] = hsv_var(blocks_list[i])

    sorted_indices = np.argsort(vars[:, 2])  # 按照第一列进行排序，返回排序后的索引
    sorted_vars = vars[sorted_indices]# 使用排序后的索引重新排列 vars
    filtered_vars = sorted_vars[sorted_vars[:,2] != 0] #过滤掉亮度为0的错误项
    #从 filtered_vars 中提取出前五个元素的第四列，并找出其中最小值的索引。
    top5 = list(filtered_vars[0:5,3])
    index = top5.index(min(top5))
    #色调方差，饱和度方差，明度方差
    print('最优子图的噪声判定:\n','色彩：',(filtered_vars[index,0]+filtered_vars[index,1])/2*10000,'明度:',filtered_vars[index,2]*10000)
    return filtered_vars[index,2]*10000   #只用亮度评判就行了

