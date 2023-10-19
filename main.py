import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
def ReadImage(name):
    print('Reading image:', name)
    img = Image.open('img/' + name + '.png').convert('L')
    return img

def PrintImageInfo(image):
    height, width = image.shape
    print(image)
    print("Minimum:", np.min(image))
    print("Maximum:", np.max(image))
    print("Height: ", height, "px", sep="")
    print("Width: ", width, "px", sep="")
    print("----------------------------------------")

def CalculateCooccurence(imgArr):
    height, width = imgArr.shape
    matrix = np.zeros((256,256), dtype=int)
    for i in range(height - 1):
        for j in range(width):
            index1 = imgArr[i][j]
            index2 = imgArr[i+1][j]
            matrix[index1][index2] += 1
    return matrix

def CalculateContrast(matrix):
    contrastNom = 0
    contrastDom = 0
    for i in range(256):
        for j in range(256):
            contrastNom += matrix[i][j] * abs(i-j)
            contrastDom += abs(i-j)
    return contrastNom / contrastDom

def CalculateHistogram(imgArr):
    histogram = np.zeros(256)
    for _ in imgArr:
        for i in _:
            histogram[i] += 1
    return histogram

def CalculateCumulativeHistogram(histogram):
    cumulativeHistogram = np.zeros(256)
    sum = 0
    for i in range(256):
        sum += histogram[i]
        cumulativeHistogram[i] = sum
    return cumulativeHistogram

def plotHistogram(histogram, title):
    plt.plot(range(256), histogram)
    plt.title(title)
    plt.show()

def GetColorAtPercentage(cumHistogram, percentage):
    value1 = cumHistogram[255] * percentage / 100
    value2 = cumHistogram[255] * (100 - percentage) / 100
    x, y = 0, 0
    for i in range(256):
        if cumHistogram[i] > value1:
            x = i - 1
            break
    for i in range(256):
        if cumHistogram[i] > value2:
            y = i - 1
            break
    return x,y

def EqualizeHistogram(imgArr, int1, int2):
    equal_img = np.copy(imgArr)
    hist = CalculateHistogram(imgArr)
    cum_hist = CalculateCumulativeHistogram(hist)
    height, width = imgArr.shape
    pixels = height * width
    for i in range(height):
        for j in range(width):
            if int1 <= imgArr[i][j] <= int2:
                equalized = 255 * cum_hist[imgArr[i][j]] / pixels
                equal_img[i][j] = equalized
    return equal_img

def GrayScaleTransformation(imgArr, x1, x2, y1, y2):
    transformedArr = np.copy(imgArr)
    height, width = imgArr.shape
    for i in range(height):
        for j in range(width):
            p = imgArr[i][j]
            if p < x1:
                transformedArr[i][j] = p * y1/x1
            elif p < x2:
                transformedArr[i][j] = ((p-x1) * (y2-y1)/(x2-x1)) + y1
            else:
                transformedArr[i][j] = ((p-x2) * (255-y2)/(255-x2)) + y2
    return transformedArr

image1 = ReadImage('image4')
img1Arr = np.array(image1)
# PrintImageInfo(img1Arr)
# cooccurence = CalculateCooccurence(img1Arr)
# # print(cooccurence)
# contrast = CalculateContrast(cooccurence)
# print("Contrast: ", contrast)
hist = CalculateHistogram(img1Arr)
plotHistogram(hist, "Histogram")
cumHist = CalculateCumulativeHistogram(hist)
plotHistogram(cumHist, "Cumulative Histogram")
plt.imshow(img1Arr, cmap='gray')
plt.show()
x1, x2 = GetColorAtPercentage(cumHist, 15)
print(x1,x2)
transformedImg = GrayScaleTransformation(img1Arr, x1, x2, 20, 190)
plt.imshow(transformedImg, cmap='gray')
plt.show()
# equalizedImg = EqualizeHistogram(img1Arr, 50,200)
# plt.imshow(equalizedImg, cmap='gray')
# plt.show()

def StretchContrast():
    pass


