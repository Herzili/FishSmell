import numpy as np
import pywt
import pywt.data
from skimage import io, img_as_float
import shared

# return 小波降噪后的图像
def atwt_main(img,outpath,threshold=0.03):
    print('F')
    print("小波变换高频降噪...")
    wtbase = 'sym4'
    迭代轮数 = 1
    image = img
    image = img_as_float(image)
    denoised_image = wavelet_denoise(image, wavelet=wtbase, threshold_factor=threshold ,level=2, iterations = 迭代轮数)
    # 导出图像
#    io.imsave(fr"{outpath}\output\atwt.tif", denoised_image.astype(np.float32))
    return denoised_image

# 小波变换去噪
def wavelet_denoise(image, wavelet, threshold_factor,level, iterations):
    # 将RGB图像分解为三个通道
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    # 对每个通道进行小波变换去噪
    def denoise_channel(channel):
        coeffs = pywt.wavedec2(channel, wavelet, level=level)
        # 创建阈值化后的系数列表
        coeffs_thresh = list(coeffs)
        # 阈值化高频部分
        for i in range(1, len(coeffs_thresh)):
            threshold = threshold_factor * np.max(coeffs_thresh[i])
            coeffs_thresh[i] = tuple(pywt.threshold(c, threshold, mode='soft') for c in coeffs_thresh[i])
        return pywt.waverec2(coeffs_thresh, wavelet)
    
    # 对每个通道进行降噪处理
    r_denoised = r
    g_denoised = g
    b_denoised = b
    
    for _ in range(iterations):
        shared.log = "小波变换高频降噪...R通道"
        r_denoised = denoise_channel(r_denoised)
        shared.log = "小波变换高频降噪...G通道"
        g_denoised = denoise_channel(g_denoised)
        shared.log = "小波变换高频降噪...B通道"
        b_denoised = denoise_channel(b_denoised)
    
    # 合并降噪后的三个通道
    denoised_image = np.stack((r_denoised, g_denoised, b_denoised), axis=-1)
    return denoised_image

