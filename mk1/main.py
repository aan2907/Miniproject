import validate
#import ocr
import alertsystem

img=r'C:\Users\cs1\Documents\MP\testdata\cropped.jpg'
plate=[]

#platenum=ocr.runOcr(img)
platenum='UP14BN4001'
print(platenum)
valid = validate.validate(platenum)
print(valid)
if valid:
    alertsystem.seandnot(valid)


