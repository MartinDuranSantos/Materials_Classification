from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import cv2
#np.set_printoptions(threshold=sys.maxsize)
#------------------------------------------------------------------------
from Co_ocurrence import *
from histogram_operator import *
#------------------------------------------------------------------------
global Matrix,Matrix_labels,Matrix2,Matrix2_labels,Matrix3,Matrix3_labels
global u,u2,u3
u=-1
u2=-1
u3=-1
Matrix3=[]
Matrix3_labels=[]

def create_Canvas(Image,xc,yc):
    canvas=Canvas(window,width=640,height=480)
    canvas.place(x=xc,y=yc)
    canvas.create_image([0, 0],anchor=NW,image=Image)
    canvas.mainloop()

def create_Entry(xc,yc):
    sal=Entry(window,font=("Courrier",20),bg='#14B77F',fg='white')
    sal.place(x=xc,y=yc)
    return sal

def create_Botton(Name,commando,xc,yc):
    Button(window, text=Name,font=("Courrier",   20),bg="white",fg="#41b77F",anchor=NW,command=commando).place(x=xc,y=yc)


def Historial(Image):
    global Matrix,Matrix_labels1,Matrix2,Matrix2_labels
    global u,u2
    Matrix.append(Image)
    return Matrix

def open_Image():
    global Original
    filename = filedialog.askopenfilename(initialdir="./Training", title="Select file",filetypes=(("jpeg files", ".jpg"), ("all files", ".*")))
    Original = cv2.imread(filename).astype(np.uint8)
    
    global Matrix,Matrix_labels
    global u
    Matrix=[]
    Matrix_labels=[]
    u=-1
    Matrix=Historial(Original)
    Matrix_labels.append("Original")

    Original_rgb = cv2.cvtColor(Original,cv2.COLOR_BGR2RGB)
    Original_tk = ImageTk.PhotoImage(image=Image.fromarray(Original_rgb))
    create_Canvas(Original_tk,350,0)
    return Original

def histogram():
    global Matrix,Matrix_labels,Matrix2,Matrix2_labels,Matrix3,Matrix3_labels
    #global u,u2
    u=2
    current=1
    if current==1:
        H=Matrix[u].astype(np.uint8)
        #print("Original: ",Original.shape)
        Salida = histogram_operator(H)
    elif current==2:
        Original=Matrix2[u2+1].astype(np.uint8)
        print("Original: ",Original.shape)
        Salida = histogram_operator(Original)
    elif current==3:
        Original=Matrix3[u3+1].astype(np.uint8)
        print("Original: ",Original.shape)
        Salida = histogram_operator(Original)
#------------------------------------------------------------------------------------------
def feature_extraction():
    global Original,features

    rgb=histogram_operator(Original.astype(np.uint8))
    rgb=np.array(rgb)
    #Salida = cv2.cvtColor(Salida, cv2.COLOR_RGB2BGR).astype(np.uint8)
    Salida = cv2.cvtColor(Original, cv2.COLOR_BGR2HSV).astype(np.uint8)
    hsv=histogram_operator(Salida.astype(np.uint8))
    hsv=np.array(hsv)
    features=np.concatenate((rgb,hsv),axis=0).reshape(1,12)

    Gray = cv2.cvtColor(Original, cv2.COLOR_BGR2GRAY).astype(np.uint8)
    M=Co_ocurrence(Gray.astype(np.uint8))
    M[0][0]=0
    
#------------------------------------------------------------------------------------------
    mu_x=0
    mu_y=0
    for i in range(0,256):
        for j in range(0,256):
            mu_x=mu_x + i*M[i,j]
            mu_y=mu_y + j*M[i,j]
    
    #print("medias: ",mu_x,mu_y)
    sigma_x=0
    sigma_y=0
    for i in range(0,256):
        for j in range(0,256):
            sigma_x=sigma_x + ((i-mu_x)**2)*M[i,j]
            sigma_y=sigma_y + ((j-mu_y)**2)*M[i,j]

    #Contrast=0
    Mean=np.mean(M)
    Maximo=np.max(M)
    #for k in range(0,256):
    Energy=0
    Variation=0
    Entropy=0
    Correlation=0
    Local_H=0
    for i in range(0,256):
        for j in range(0,256):
            Energy=Energy + (M[i,j]**2)
            Variation=Variation + ((i-Mean)**2)*(M[i,j]**2)
            if M[i,j]!=0:
                Entropy=Entropy + M[i,j]*np.log(M[i,j]) 
            #Contrast=Contrast + (k**2)*(M[i,j])
            Correlation=Correlation + (M[i,j]-(mu_x*mu_y))/(sigma_x*sigma_y)
            den=1-abs(i-j) 
            if den!=0: 
                Local_H=Local_H + (M[i,j]/den)

    features2=np.array([Mean,Maximo,Energy,Variation,Entropy,Correlation,
Local_H]).reshape(1,7)     

    features=np.concatenate((features,features2),axis=1).reshape(1,19)   

    from tkinter import messagebox

    messagebox.showinfo("Title", "19 features were succesfully extracted from current image")

#------------------------------------------------------------------------------------------
global FMatrix
FMatrix=[]
global indice
indice=1
def train():
    import pandas as pd
    from pandas import ExcelWriter
    from pandas import ExcelFile
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    global FMatrix,features,indice,clas
    ccc=np.zeros([1,1])
    clase=int(clas.get())
    ccc[0,0]=clase
    vector=np.concatenate((features,ccc),axis=1)
    FMatrix.append(vector.reshape(1,20))
    F_train=np.array(FMatrix).reshape(indice,20)

    df = pd.DataFrame(F_train,columns = ['xr', 'red','xg','green','xb','blue','xh','hue','xs','saturation','xv','v',"Mean","Maximo","Energy","Variation","Entropy","Correlation","Local_H",'Salida'])
    df.to_excel(r'Db.xlsx', index = False)
    

    from tkinter import messagebox

    messagebox.showinfo("Title", "Train succesful: " + str(indice) + " Observations")
    indice=indice+1

#------------------------------------------------------------------------------------------
window=Tk()
window.title("My app")
window.geometry("1800x1000")
window.config(background="#41B77F")

global var,var2,var3
global opciones,opciones2,opciones3

create_Botton("Open Image",open_Image,0,0)
create_Botton("Features Extraction",feature_extraction,0,200)

global clas
clas=create_Entry(0,400)
create_Botton("Train",train,0,450)
#-----------------------------------------------------------------------------------
window.mainloop()
