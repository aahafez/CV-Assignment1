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
    pass

def StretchContrast(imageArr, c, d):
    a = 0
    b = 255
    height, width = imageArr.shape
    newImage = Image.new('L', (width, height))
    for i in range(height):
        for j in range(width):
            newImage.putpixel((j,i), int((imageArr[i,j] - c) * ((b-a) / (d - c)) + a))
    return newImage

def EqualizeHistogram():
    pass

def GrayScaleTransformation():
    pass

image1 = ReadImage('image4')
img1Arr = np.array(image1)
PrintImageInfo(img1Arr)
cooccurence = CalculateCooccurence(img1Arr)
# print("Cooccurence: ", cooccurence)
contrast = CalculateContrast(cooccurence)
print("Contrast: ", contrast)
hist = CalculateHistogram(img1Arr)
plotHistogram(hist, "Histogram")
cumHist = CalculateCumulativeHistogram(hist)
plotHistogram(cumHist, "Cumulative Histogram")
c = input("Please enter value for c \n")
d = input("Please enter value for d \n")
contrastStretch = StretchContrast(img1Arr, int(c), int(d))
plt.imshow(contrastStretch, cmap = "gray")
plt.show()
print("Done:)")