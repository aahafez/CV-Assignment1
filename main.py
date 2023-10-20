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
    pixels = cum_hist[-1]
    int_max = max(int1, int2)
    f_min = cum_hist[min(int1, int2)]
    for i in range(height):
        for j in range(width):
            # if int1 <= imgArr[i][j] <= int2:
            equalized = int_max * (cum_hist[imgArr[i][j]] - f_min) / (pixels - f_min)
            if equalized < 0:
                equalized = 0
            elif equalized > 255:
                equalized = 255
            equal_img[i][j] = equalized
    plt.imshow(equal_img, cmap="gray")
    plt.title("Post histogram equalization")
    plt.show()
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
    plt.imshow(transformedArr, cmap="gray")
    plt.title("Post grayscale transformation")
    plt.show()
    return transformedArr

def StretchContrast(imageArr, a, b, c, d):
    height, width = imageArr.shape
    newImage = Image.new('L', (width, height))
    for i in range(height):
        for j in range(width):
            newImage.putpixel((j,i), int((imageArr[i,j] - c) * ((b-a) / (d - c)) + a))
    plt.imshow(newImage, cmap="gray")
    plt.title("Post contrast stretching")
    plt.show()
    return newImage

def plotHistograms(imgArr, title):
    hist = CalculateHistogram(imgArr)
    plotHistogram(hist, title + " Histogram")
    cumHist = CalculateCumulativeHistogram(hist)
    plotHistogram(cumHist, title + " Cumulative Histogram")
    return cumHist

def test(imgName,percentage):
    # Read image and convert it to a 2D Array
    img = ReadImage(imgName)
    imgArr = np.array(img)
    # Calculate cooccurence, contrast and plot both histograms
    cooccurence = CalculateCooccurence(imgArr)
    contrast = CalculateContrast(cooccurence)
    print("Contrast: ", contrast)
    cumHist = plotHistograms(imgArr, "Original")
    # Test Color at percentage with given percentage parameter
    x, y = GetColorAtPercentage(cumHist, percentage)
    print("X:", x)
    print("Y:", y)
    # Test contrast stretching and plot corresponding histograms
    contrastStretch = StretchContrast(imgArr, 0, 255, x, y)
    plotHistograms(np.array(contrastStretch), "Post contrast stretch")
    # Test histogram equalization and plot corresponding histograms
    equalHist = EqualizeHistogram(imgArr, x, y)
    plotHistograms(equalHist, "Post histogram equalization")
    # Test grayscale transformation and plot corresponding histograms
    grayscaleTrans = GrayScaleTransformation(imgArr, x, y,0,255)
    plotHistograms(grayscaleTrans, "Post grayscale transformation")
    # Print test is done
    text = "TEST IS DONE"
    print(f'{text:-^40}')

def groundTruth():
    # Read image and convert it to a 2D Array
    img = ReadImage('image4')
    imgArr = np.array(img)
    # Calculate cooccurence, contrast and plot both histograms
    cooccurence = CalculateCooccurence(imgArr)
    contrast = CalculateContrast(cooccurence)
    print("Contrast: ", contrast)
    cumHist = plotHistograms(imgArr, "Original")
    x, y = 88, 151
    print("X:", x)
    print("Y:", y)
    # Test contrast stretching and plot corresponding histograms
    contrastStretch = StretchContrast(imgArr, 0, 255, x, y)
    plotHistograms(np.array(contrastStretch), "Post contrast stretch")
    # Test histogram equalization and plot corresponding histograms
    equalHist = EqualizeHistogram(imgArr, x, y)
    plotHistograms(equalHist, "Post histogram equalization")
    # Test grayscale transformation and plot corresponding histograms
    grayscaleTrans = GrayScaleTransformation(imgArr, x, y,0,255)
    plotHistograms(grayscaleTrans, "Post grayscale transformation")
    # Print test is done
    text = "GROUND TRUTH TEST IS DONE"
    print(f'{text:-^40}')

test('image4', 5)
# groundTruth()