import easyocr
import cv2
import warnings
warnings.filterwarnings('ignore')

def preprocess(image):
    image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #grayscale
    image= cv2.medianBlur(image,1)  #noise removal
    if(image.shape[0]>1200 and image.shape[1]>1500):
        image= cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)   #adaptive thresholding
        image= cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]  #thresholding
        image= cv2.dilate(image, np.ones((5,5),np.uint8), iterations = 1)  #dilation
        image= cv2.erode(image, np.ones((5,5),np.uint8), iterations = 1)  #erosion
        image= cv2.morphologyEx(image, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))  #opening - erosion followed by dilation
        image= cv2.Canny(image, 100, 200)  #canny edge detection
        image= cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)  #template matching
    return image

def runOcr(img_path):
    img= cv2.imread(img_path)
    img= preprocess(img)
    reader= easyocr.Reader(['en'])
    result= reader.readtext(img, mag_ratio=2, text_threshold=0.2, min_size=1, low_text=0.3, detail= 0)
    result= ' '.join([str(elem) for elem in result])
    return result

print(runOcr(r"C:\Users\ASUS\Programming\Untitled Folder\ocrtest.jpg"))