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
    if(img.shape[0]>1200 and img.shape[1]>1500):
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]      #binarize
        #img = cv2.erode(img,np.ones((1,1),np.uint8),iterations = 1)     #thinning
    #display(img, 'noise')
    return img

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
    return ocr(img), img.shape
