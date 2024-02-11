from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import cv2

from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import cv2

def Co_ocurrence(image):
    M=np.zeros([256,256])
    fil,col=image.shape

    for f in range(0,fil):
        for c in range(0,col):
            vant=int(image[f,c])
            if c<col-1:
                vsig=int(image[f,c+1])
            else:
                break
 
            M[vant][vsig]=M[vant][vsig]+1


    return M
