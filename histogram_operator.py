from PIL import Image, ImageTk
import numpy as np
import cv2
from matplotlib import pyplot as plt

def histogram_operator(noise_img):
    tipo =len(noise_img.shape)
    xvector=np.linspace(0,255,256)
    sal=np.zeros([3,2])
    ind=2
    if tipo==3:
        color = ('b','g','r')
        #color = ('r','g','b')
    elif tipo==2:
        color = ('k')
    for i,col in enumerate(color):
        #print("i: ",i)
        #histr = cv2.calcHist([noise_img],[i],None,[256],[0,256])
        histr = cv2.calcHist([noise_img],[i],None,[255],[1,256])
        #plt.plot(histr,color = col)
        #print(histr.shape)
        #print(histr)
        sal[ind,1]=max(histr)
        h=histr.tolist()
        sal[ind,0]=h.index(sal[ind,1])
        
        #sal[:,ind]=histr.reshape(255,)
        #plt.bar(xvector,histr,color = col)
        #plt.title("Histogram")
        #plt.xlabel("scale")
        #plt.ylabel("number of pixels")
        #plt.xlim([1,256])
        ind=ind-1
    #print(sal)
    #plt.show()
    return sal
