from skimage import io,color
import numpy as np
from numba import jit
import shared

#传入已经 色平衡, DBE 过的图像
@jit
def mid (m,pic):#拉伸调整中间滑块
    for i in range(pic.shape[0]):
        for j in range(pic.shape[1]):
            tmp  = pic[i,j]
            pic[i,j] = (m-1)*tmp/((2*m-1)*tmp -m)
    return pic

@jit
def but (b,pic):#拉伸截取明度屁股
    for i in range(pic.shape[0]):
        for j in range(pic.shape[1]):
            if pic[i,j] >= b:
                pic[i,j] = (pic[i,j] - b)*(1/(1-b))
            else :
                pic[i,j] = 0
    return pic

#return 拉伸后的图片
def pull_main(inpath,outpath):
    print("自动拉伸...")
    shared.log = "自动拉伸..."
    #可调参数
    BIN = 2048  #最低支持12bit色深
    归一化数值 = 1
    #分离RGB，获取图片格式情况。
    image = io.imread(fr"{inpath}")   #目前是numpy数组
    R = image[:, :, 0]  # 红色通道(0-65535)
    G = image[:, :, 1]  # 绿色通道
    B = image[:, :, 2]  # 蓝色通道
    print(R.max())
    if R.max() <=1:     #浮点
        归一化数值 = 1
    elif R.max() >40000 and R.max() <65536: #16bit整形
        归一化数值 = 65535
    else :
        print(f'错误: 图像最大明度{R.max()},只支持16bit色深，或浮点格式图像。')
        exit()

    print("归一化数值是",归一化数值)

    #推算尾截点butt
    gray_image = R/归一化数值 #使用R通道作为拉伸评判
    img_255 = (gray_image * (BIN-1)).astype(np.uint16)
    hist, bin_edges = np.histogram(img_255, bins=BIN, range=(0,BIN-1))
    peak = np.argmax(hist)
    print(hist)
    print("peask的索引值为: ",peak)
    tmp_1 = peak - 2
    while(True):
        if  hist[tmp_1-1] < (hist[tmp_1]+ hist[tmp_1+1]+ hist[tmp_1+2])/3 and hist[tmp_1-1] > 0.003* hist[peak]:
            tmp_1 = tmp_1 - 1
        else:
            break
    butt = tmp_1*0.995
    butt /= BIN-1
    print('尾部滑块',butt)

    切屁股的归一化R通道 = but(butt,gray_image)

    #推算中间点middle，先but后再推算
    img_255 = (切屁股的归一化R通道 * (BIN-1)).astype(np.uint16)#获取255灰度图
    hist, bin_edges = np.histogram(img_255, bins=BIN, range=(0, BIN-1))
    peak = np.argmax(hist)
    tmp_2 = peak+10
    while(True):
        if  hist[tmp_2+ 10] < (hist[tmp_2]+ hist[tmp_2-10])/2 and hist[tmp_2 + 10] > 0.02* hist[peak] and tmp_2+10 < BIN-1:
            tmp_2 = tmp_2 + 10
        else:
            break
    middle = tmp_2/(BIN-1)
    print('中间滑块',middle)

    #拉伸三个通道
    拉伸完毕的R通道 = mid(middle,切屁股的归一化R通道)

    gray_image = G/归一化数值
    切屁股的归一化G通道 = but(butt,gray_image)
    拉伸完毕的G通道 = mid(middle,切屁股的归一化G通道)


    gray_image = B/归一化数值
    切屁股的归一化B通道 = but(butt,gray_image)
    拉伸完毕的B通道 = mid(middle,切屁股的归一化B通道)

    #还原RGB图像
    back_image = np.dstack((拉伸完毕的R通道,拉伸完毕的G通道,拉伸完毕的B通道))
    back_image = back_image.astype(np.float32)
#    io.imsave(fr"{outpath}\output\pull.tif", back_image)
    return back_image