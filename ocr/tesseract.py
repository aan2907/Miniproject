import cv2, os
import pytesseract
from pytesseract import Output
import numpy as np

def ocr(img):
    #text = pytesseract.image_to_string(img)
    custom_config = r'--oem 3 --psm 4'
    boxes = pytesseract.image_to_data(img, config=custom_config, output_type=Output.DICT)
    return boxes

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
    display(image, 'Preprocessed')
    return image


def visualise(img_path, results):
    img = cv2.imread(img_path)
    y, x, c = img.shape
    print(x, y)
    for (bbox, text, prob) in results:
        #print("[INFO] {:.4f}: {}".format(prob, text))
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        #text = cleanup_text(text)
        cv2.rectangle(img, tl, br, (0, 0, 255), 2)
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
            with open(os.path.join(r'E:\Mess\Queo\main\results\ocrresults', image + '.txt'), 'r') as res:
                wordlist = eval(res.read())
                return [list(a) for a in wordlist], img.shape
        except FileNotFoundError:
            pass
    img = preprocess(img)
    boxes = ocr(img)
    wordlist=[]
    n_boxes = len(boxes['text'])
    for i in range(n_boxes):
        text=boxes['text'][i]
        line_num=boxes['line_num'][i]
        x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
        a, b, c, d=[x, y], [x+w, y], [x+w, y+h],[x, y+h]
        wordlist.append([[a, b, c, d], text, line_num])
    return wordlist, img.shape




