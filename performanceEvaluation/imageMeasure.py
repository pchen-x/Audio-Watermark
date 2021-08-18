# LIBRARIES

import cv2
import numpy as np


# -----------------------------------------

# FUNCTIONS

# Mean square error
def MSE(imgA, imgB):
    rows, cols = imgA.shape
    sumimg = 0
    for i in range(rows):
        for j in range(cols):
            sumimg = sumimg + ((float(imgA[i, j]) - float(imgB[i, j])) ** 2)
    return sumimg / (rows * cols)


# Peak signal to noise ratio
def PSNR(imgA, imgB):
    rows, cols = imgA.shape
    sumimg = 0
    for i in range(rows):
        for j in range(cols):
            sumimg = sumimg + ((float(imgA[i, j]) - float(imgB[i, j])) ** 2)
    mse = sumimg / (rows * cols)
    const = 255 ** 2
    frac = float(const / mse)
    return 10 * np.log10(frac)


# average difference
def avgDiff(imgA, imgB):
    rows, cols = imgA.shape
    sumimg = 0
    for i in range(rows):
        for j in range(cols):
            sumimg = sumimg + (float(imgA[i, j]) - float(imgB[i, j]))
    return sumimg / (rows * cols)


# Normalized correlation
def normalizedCorrelation(imgA, imgB):
    rows, cols = imgA.shape
    sqrAsum = 0
    productsum = 0
    for i in range(rows):
        for j in range(cols):
            productsum = productsum + (float(imgA[i, j]) * float(imgB[i, j]))
            sqrAsum = sqrAsum + ((float(imgA[i, j])) ** 2)

    return productsum / sqrAsum


# Maximum Difference

def maxDiff(imgA, imgB):
    diff = np.absolute(imgA.astype('float') - imgB.astype('float'))
    return np.amax(diff)


# Normalized Absolute error
def normalizedAbsoluteError(imgA, imgB):
    rows, cols = imgA.shape
    Asum = 0
    productsum = 0
    for i in range(rows):
        for j in range(cols):
            product = abs(float(imgA[i, j]) - float(imgB[i, j]))
            productsum = productsum + product
            Asum = Asum + abs(float(imgA[i, j]))
    return productsum / (Asum)


# Structural Content
def structuralContent(imgA, imgB):
    rows, cols = imgA.shape
    Asum = 0
    Bsum = 0
    for i in range(rows):
        for j in range(cols):
            Asum = Asum + (float(imgA[i, j])) ** 2
            Bsum = Bsum + (float(imgB[i, j])) ** 2

    return Asum / Bsum


# SSIM Structural SIMilarity Index (SSIM).
def ssim(imgA, imgB):
    def __get_kernels():
        k1, k2, l = (0.01, 0.03, 255.0)
        kern1, kern2 = map(lambda x: (x * l) ** 2, (k1, k2))
        return kern1, kern2

    def __get_mus(i1, i2):
        mu1, mu2 = map(lambda x: __gaussian_filter(x, 1.5), (i1, i2))
        m1m1, m2m2, m1m2 = (mu1 * mu1, mu2 * mu2, mu1 * mu2)
        return m1m1, m2m2, m1m2

    def __get_sigmas(i1, i2, delta1, delta2, delta12):
        f1 = __gaussian_filter(i1 * i1, 1.5) - delta1
        f2 = __gaussian_filter(i2 * i2, 1.5) - delta2
        f12 = __gaussian_filter(i1 * i2, 1.5) - delta12
        return f1, f2, f12

    def __get_positive_ssimap(C1, C2, m1m2, mu11, mu22, s12, s1s1, s2s2):
        num = (2 * m1m2 + C1) * (2 * s12 + C2)
        den = (mu11 + mu22 + C1) * (s1s1 + s2s2 + C2)
        return num / den

    def __get_negative_ssimap(C1, C2, m1m2, m11, m22, s12, s1s1, s2s2):
        (num1, num2) = (2.0 * m1m2 + C1, 2.0 * s12 + C2)
        (den1, den2) = (m11 + m22 + C1, s1s1 + s2s2 + C2)
        ssim_map = __n.ones(img1.shape)
        indx = (den1 * den2 > 0)
        ssim_map[indx] = (num1[indx] * num2[indx]) / (den1[indx] * den2[indx])
        indx = __n.bitwise_and(den1 != 0, den2 == 0)
        ssim_map[indx] = num1[indx] / den1[indx]
        return ssim_map

    (img1, img2) = (imgA.astype('double'), imgB.astype('double'))
    (m1m1, m2m2, m1m2) = __get_mus(img1, img2)
    (s1, s2, s12) = __get_sigmas(img1, img2, m1m1, m2m2, m1m2)
    (C1, C2) = __get_kernels()
    if C1 > 0 and C2 > 0:
        ssim_map = __get_positive_ssimap(C1, C2, m1m2, m1m1, m2m2, s12, s1, s2)
    else:
        ssim_map = __get_negative_ssimap(C1, C2, m1m2, m1m1, m2m2, s12, s1, s2)
    ssim_value = ssim_map.mean()
    return ssim_value
