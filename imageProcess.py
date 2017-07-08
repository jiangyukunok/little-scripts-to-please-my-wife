'''
The texts in one of amazon product pics are not clear enough, so write a simple script to highlight texts.
'''
from PIL import Image


def isDesc(sample):
  return sample[0]>180 and sample[0]<230 and sample[1]<240 and sample[1]>180 and sample[2]<225 and sample[2]>190


im = Image.open("/Users/jiangyukun/Downloads/1.jpg")
pix = im.load()
imgSize = im.size
for row in range(0, imgSize[0]):
  for col in range(0, imgSize[1]):
    sample = pix[row, col]
    if isDesc(sample):
      pix[row, col] = (0,0,0)

im.save("/Users/jiangyukun/Downloads/2.jpg")
