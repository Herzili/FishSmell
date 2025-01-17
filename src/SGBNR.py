import numpy as np
from skimage import io, filters
from skimage.color import rgb2lab, lab2rgb
from skimage import  img_as_float
import shared

def generate_constant_gray_mask(image, mask_value=0.5):
    # 创建与图像相同尺寸的纯色蒙版
    mask = np.full(image.shape[:2], mask_value)  # 图像的大小与输入图像相同，所有像素的值为mask_value
    return mask

def selective_gaussian_blur(image, mask, kernel_size=5):
    blurred_image = filters.gaussian(image, sigma=kernel_size)
    result = mask * image + (1 - mask) * blurred_image  # 蒙版值越大，原图像影响越大，降噪越弱
    return result

def apply_sgbnr_to_lab(image, ab_mask_value,l_mask_value,kernel_l,kernel_a,kernel_b):
    print(f"正在SGBNR降噪...轮数为{shared.循环次数}")
    # 1. 转换RGB图像到Lab色彩空间
    lab_image = rgb2lab(image)
    # 2. 提取L、a和b通道
    l_channel = lab_image[:, :, 0]  # 亮度通道
    a_channel = lab_image[:, :, 1]  # 绿色-红色通道
    b_channel = lab_image[:, :, 2]  # 蓝色-黄色通道
    
    ab_mask = generate_constant_gray_mask(image, ab_mask_value)
    l_mask = generate_constant_gray_mask(image, l_mask_value)
    # 3. 对L、a、b通道分别应用选择性高斯模糊降噪

    for i in range(shared.循环次数):
        print("正在SGBNR降噪...L通道")
        l_channel = selective_gaussian_blur(l_channel, l_mask,  kernel_l*(i+1))
        print("正在SGBNR降噪...a通道")
        a_channel = selective_gaussian_blur(a_channel, ab_mask,  kernel_a*(i+1))
        print("正在SGBNR降噪...b通道")
        b_channel = selective_gaussian_blur(b_channel, ab_mask,  kernel_b*(i+1))
    
    # 4. 将降噪后的L、a、b通道替换原图中的通道
    lab_image[:, :, 0] = l_channel
    lab_image[:, :, 1] = a_channel
    lab_image[:, :, 2] = b_channel
    
    # 5. 转换回RGB图像
    denoised_image = lab2rgb(lab_image)
    
    return denoised_image

def sgbnr_main(img,outpath,ab_mask_value=0,l_mask_value=0, kernel_l=1,kernel_a=11,kernel_b=11):
    print('H')
    image = img
    image_float = img_as_float(image)
    # 降噪，分离Lab通道进行处理
    denoised_image = apply_sgbnr_to_lab(image_float,  ab_mask_value=ab_mask_value, l_mask_value=l_mask_value,  kernel_l=kernel_l,kernel_a=kernel_a,kernel_b=kernel_b)
    # 保存降噪后的图像（可选）
    try:
        io.imsave(fr"{outpath}\output\鱼香肉丝.png", np.uint8(denoised_image*255))
        denoised_image = np.uint16(denoised_image* 65535)  
        io.imsave(fr"{outpath}\output\鱼香肉丝.tif", denoised_image)
    except:
        print('\033[35mSGBNR.py: 输出路径有问题,稍后重试\033[37m')

    print("已输出 鱼香肉丝.tif！")
    return denoised_image #后续接口