import cv2, os
import pytesseract
from pytesseract import Output
import numpy as np
import warnings
warnings.filterwarnings('ignore')

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def display(img, window):
    y, x= img.shape
    if y>1000:
        x=int(1000*x/y)
        y=1000
    img = cv2.resize(img, (x, y), interpolation = cv2.INTER_AREA)
    cv2.imshow(window, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preprocess(image, width=120, height=50):
    #image=cv2.resize(image, (width, height))
    image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #grayscale
    image= cv2.medianBlur(image,1)  #noise removal
    image= cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)   #adaptive thresholding
    #image= cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  #thresholding
    #image= cv2.dilate(image, np.ones((5,5),np.uint8), iterations = 1)  #dilation
    #image= cv2.erode(image, np.ones((5,5),np.uint8), iterations = 1)  #erosion
    #image= cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))  #opening - erosion followed by dilation
    #image= cv2.Canny(image, 100, 200)  #canny edge detection
    #image= cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)  #template matching
    return image

def preprocess(image, width=120, height=50):
    #image=cv2.resize(image, (width, height))
    image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #grayscale
    image= cv2.medianBlur(image,1)  #noise removal
    image= cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)   #adaptive thresholding
    #image= cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  #thresholding
    #image= cv2.dilate(image, np.ones((5,5),np.uint8), iterations = 1)  #dilation
    #image= cv2.erode(image, np.ones((5,5),np.uint8), iterations = 1)  #erosion
    #image= cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))  #opening - erosion followed by dilation
    #image= cv2.Canny(image, 100, 200)  #canny edge detection
    #image= cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)  #template matching
    #display(image, "preprocessed")
    return image


def runOcr(img_path, testing=False):
    img = cv2.imread(img_path)
    img = preprocess(img)
    text = pytesseract.image_to_string(img)
    return text

print(runOcr(r"C:\Users\Ahad\Desktop\plate.jpeg"))





