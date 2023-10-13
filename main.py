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
def CalculateCooccurence(image):
    imgArr = np.array(image)
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

image1 = ReadImage('image1')
PrintImageInfo(np.array(image1))
cooccurence = CalculateCooccurence(image1)
# print(cooccurence)
contrast = CalculateContrast(cooccurence)
print("Contrast: ", contrast)

def CalculateHistogram():
    pass

def CalculateCumulativeHistogram():
    pass

def GetColorAtPercentage():
    pass

def StretchContrast():
    pass

def EqualizeHistogram():
    pass

def GrayScaleTransformation():
    pass

