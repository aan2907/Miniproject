import easyocr, os
import numpy as np
import cv2
import warnings
warnings.filterwarnings('ignore')

def ocr(img):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img, mag_ratio=2, text_threshold=0.2, min_size=1, low_text=0.3)
    return [list(a) for a in result]

def display(img, window):
    y, x, c = img.shape
    if y>1000:
        x=int(1000*x/y)
        y=1000
    img = cv2.resize(img, (x, y), interpolation = cv2.INTER_AREA)
    cv2.imshow(window, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preprocess(img):
    #img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)      #noise reduction
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        #grayscale
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]      #binarize
        #img = cv2.erode(img,np.ones((1,1),np.uint8),iterations = 1)     #thinning
    #display(img, 'noise')
    return img

def runOcr(img_path):
    img = cv2.imread(img_path)
    img = preprocess(img)
    words=ocr(img)
    if len(words)>=1:
        return words[0][1]
    else:
        return None

print(runOcr(r"C:\Users\cs1\Documents\mk1\anpr\runs\detect\predict\crops\license-plate\demo4.jpg"))

