import time
import paddleoc
import easy

path = r'E:\Mess\Queo\main\testdata\digital\digital02.JPG'

t=time.time()
wordlist, shape=paddleoc.runOcr(path)
print("PaddleOCR :", time.time()-t)
t2=time.time()
wordlist, shape=easy.runOcr(path)
print("EasyOCR :", time.time()-t2)