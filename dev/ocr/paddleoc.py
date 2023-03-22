from paddleocr import PaddleOCR
import numpy as np
import cv2, os
import warnings
warnings.filterwarnings('ignore')

testpath=r'E:\Mess\Queo\main\results\ocrresults'

def ocr(img_path):
    ocr = PaddleOCR(lang='en', show_log=False)
    res=ocr.ocr(img_path)[0]
    return [[i[0], i[1][0]] for i in res]

def display(img, window):
    y, x= img.shape
    if y>1000:
        x=int(1000*x/y)
        y=1000
    img = cv2.resize(img, (x, y), interpolation = cv2.INTER_AREA)
    cv2.imshow(window, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preprocess(image):
    image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #grayscale
    image=cv2.medianBlur(image,1)  # noise removal
    if(image.shape[0]>1200 and image.shape[1]>1500):
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)   #adaptive thresholding
        #image=cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  #thresholding
        #image=cv2.dilate(image, np.ones((5,5),np.uint8), iterations = 1)  #dilation
        #image=cv2.erode(image, np.ones((5,5),np.uint8), iterations = 1)  #erosion
        #image=cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))  #opening - erosion followed by dilation
        #image=cv2.Canny(image, 100, 200)  #canny edge detection
        #image=cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)  #template matching
    #display(image, 'Preprocessed')
    return image


def visualise(img_path, results):
    img = cv2.imread(img_path)
    y, x, c = img.shape
    for bbox in results:
        cv2.polylines(img, [np.array(bbox[0], np.int32)], True, (0,255,0), thickness=3)
        #cv2.putText(img, text, (tl[0], tl[1] - 10),
        #    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    if y>1000:
        x=int(1000*x/y)
        y=1000
    img = cv2.resize(img, (x, y), interpolation = cv2.INTER_AREA)
    cv2.imshow("Image", img)
    cv2.waitKey(0)

def runOcr(img_path, testing=False):
    img = cv2.imread(img_path)
    if testing:
        image=img_path.split('\\')[-1][:-4]
        try:
            with open(os.path.join(testpath, image + '.txt'), 'r') as res:
                wordlist = eval(res.read())
                return [list(a) for a in wordlist], img.shape
        except FileNotFoundError:
            pass
    img = preprocess(img)
    words = ocr(img_path)
    return words, img.shape

