import cv2
import random
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os


def my_filebrowser():
    root = tk.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    imgfile = filedialog.askopenfilename(initialdir = "testing",title = "Select Image",filetypes = (("Img files","*.jpeg"),("all files","*.jpg")))
    root.destroy()
    return imgfile

def create_stack(accno,drive):

    file_name = my_filebrowser()

    print(file_name)

    tok=file_name.split('/')
    print(tok)

    inputfile  = tok[-1]  ##'150001.jpeg';

    im_gray = cv2.imread(inputfile , cv2.IMREAD_GRAYSCALE)
    (thresh, I) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY)

    Iblank = cv2.imread("blk.bmp", cv2.IMREAD_GRAYSCALE)
    Iblank2 = cv2.imread("blk2.bmp", cv2.IMREAD_GRAYSCALE)
    #(thresh, Iblank) = cv2.threshold(Iblank, 128, 255, cv2.THRESH_BINARY)

    fname=inputfile.split('.')

    signfile=accno+".bmp"
    ##cv2.imshow('Img',I)



    ##cv2.waitKey()

    I=I//255
    info=I.shape
    rows, cols = (info[0], info[1])
    #share1 = [[0]*cols*2]*rows*2
    #share2 = [[0]*cols*2]*rows*2

    share1 = Iblank[0:rows*2,0:cols*2]  ##np.zeros((rows*2,cols*2), dtype=[('x', 'int'), ('y', 'int')])
    share2 = Iblank2[0:rows*2,0:cols*2]  ##np.zeros((rows*2,cols*2), dtype=[('x', 'int'), ('y', 'int')])

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #generating Share1 for BW image
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ii=0;

    for i in range(info[0]):
        jj=0;
        for j in range(info[1]):
            r1 = random.randint(0, 10)

            t= r1%6+1

            
            if I[i][j]==0:    #black

                #print(ii,"1 Black")
                match t:
                    case 1:
                            share1[ii][jj]=1;     share1[ii+1][jj]=0
                            share1[ii][jj+1]=1;   share1[ii+1][jj+1]=0
                    case 2:
                            share1[ii][jj]=0;    share1[ii+1][jj]=1;
                            share1[ii][jj+1]=0;  share1[ii+1][jj+1]=1;
                    case 3:
                            share1[ii][jj]=1;  share1[ii+1][jj]=1;
                            share1[ii][jj+1]=0;  share1[ii+1][jj+1]=0;
                    case 4:
                            share1[ii][jj]=0;  share1[ii+1][jj]=0;
                            share1[ii][jj+1]=1;  share1[ii+1][jj+1]=1;
                    case 5:
                            share1[ii][jj]=0;  share1[ii+1][jj]=1;
                            share1[ii][jj+1]=1;  share1[ii+1][jj+1]=0;
                    case 6:
                            share1[ii][jj]=1;  share1[ii+1][jj]=0;
                            share1[ii][jj+1]=0;  share1[ii+1][jj+1]=1;
            else:
                #print(ii,"1 white")
                match t:
                    case 1:
                            
                            

                            share1[ii][jj]=1;    share1[ii+1][jj]=0;
                            share1[ii][jj+1]=1;  share1[ii+1][jj+1]=0;
                            #print(ii,jj,share1[ii][jj],share1[ii+1][jj],share1[ii][jj+1],share1[ii+1][jj+1]);
                    case 2:
                            share1[ii][jj]=0;    share1[ii+1][jj]=1;
                            share1[ii][jj+1]=0;  share1[ii+1][jj+1]=1;
                    case 3:
                            share1[ii][jj]=1;    share1[ii+1][jj]=1;
                            share1[ii][jj+1]=0;  share1[ii+1][jj+1]=0;
                    case 4:
                            share1[ii][jj]=0;    share1[ii+1][jj]=0;
                            share1[ii][jj+1]=1;  share1[ii+1][jj+1]=1;
                    case 5:
                            share1[ii][jj]=0;    share1[ii+1][jj]=1;
                            share1[ii][jj+1]=1;  share1[ii+1][jj+1]=0;
                    case 6:
                            share1[ii][jj]=1;  share1[ii+1][jj]=0;
                            share1[ii][jj+1]=0;  share1[ii+1][jj+1]=1;
                
             
            if I[i][j]==0:    #black
                
                #print(ii,"2 Black")
                match t:
                    case 1:
                           

                            share2[ii][jj]=1;  share2[ii+1][jj]=0;
                            share2[ii][jj+1]=1;  share2[ii+1][jj+1]=0;
                    case 2:
                            share2[ii][jj]=0;  share2[ii+1][jj]=1;
                            share2[ii][jj+1]=0;  share2[ii+1][jj+1]=1;
                    case 3:
                            share2[ii][jj]=1;  share2[ii+1][jj]=1;
                            share2[ii][jj+1]=0;  share2[ii+1][jj+1]=0;
                    case 4:
                            share2[ii][jj]=0;  share2[ii+1][jj]=0;
                            share2[ii][jj+1]=1;  share2[ii+1][jj+1]=1;
                    case 5:
                            share2[ii][jj]=0;  share2[ii+1][jj]=1;
                            share2[ii][jj+1]=1;  share2[ii+1][jj+1]=0;
                    case 6:
                            share2[ii][jj]=1;  share2[ii+1][jj]=0;
                            share2[ii][jj+1]=0;  share2[ii+1][jj+1]=1;

                
                
            else:    #WHITE
                #print(ii,"2 White")
                match t:
                    case 1:
                            
                            share2[ii][jj]=0;  share2[ii+1][jj]=1;
                            share2[ii][jj+1]=0;  share2[ii+1][jj+1]=1;

                            #print(ii,jj,share2[ii][jj],share2[ii+1][jj],share2[ii][jj+1],share2[ii+1][jj+1]);
                            
                    case 2:
                            share2[ii][jj]=1;  share2[ii+1][jj]=0;
                            share2[ii][jj+1]=1;  share2[ii+1][jj+1]=0;
                    case 3:
                            share2[ii][jj]=0;  share2[ii+1][jj]=0;
                            share2[ii][jj+1]=1;  share2[ii+1][jj+1]=1;
                    case 4:
                            share2[ii][jj]=1;  share2[ii+1][jj]=1;
                            share2[ii][jj+1]=0;  share2[ii+1][jj+1]=0;
                    case 5:
                            share2[ii][jj]=1;  share2[ii+1][jj]=0;
                            share2[ii][jj+1]=0;  share2[ii+1][jj+1]=1;
                    case 6:
                            share2[ii][jj]=0;  share2[ii+1][jj]=1;
                            share2[ii][jj+1]=1;  share2[ii+1][jj+1]=0;

            

            

            jj=jj+2;

        ii=ii+2;

    ##    print(share1[ii-2:ii,jj-2:jj])
    ##    print(share2[ii-2:ii,jj-2:jj])

       
       ## print('Wait ...');

    ##cv2.imshow(I);
    ##share1 = np.array(share1)

    oshare1=share1*255
    oshare2=share2*255

    share1=share1*255
    share2=share2*255



    cv2.imshow('Share 1',share1)
    cv2.waitKey(1)

    ##share2 = np.array(share2)
    cv2.imshow('Share 2',share2);
    cv2.waitKey(1)

    ##print('Share 1')
    ##print(share1[0:4,0:4])
    ##
    ##print('Share 2')
    ##print(share2[0:4,0:4])
    sh1fname=fname[0]+"_share1.bmp"
    tempsh2fname=fname[0]+"_share2.bmp"
    sh2fname="H:\\"+fname[0]+"_share1.bmp"

    print("Storing in "+sh2fname)
                
    cv2.imwrite(sh1fname,share1);
    cv2.imwrite(sh2fname,share2);
    cv2.imwrite(tempsh2fname,share1);

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    share1 = accno+'_share1.bmp';

    share2 = accno+'_share2.bmp';

    print("@@@"+share1)

    I1 = cv2.imread(share1, cv2.IMREAD_GRAYSCALE);

    info1=I1.shape
    rows1, cols1 = (info1[0], info1[1])

    I2 = cv2.imread(share2, cv2.IMREAD_GRAYSCALE);
    info2=I2.shape
    rows2, cols2 = (info2[0], info2[1])

     


    (thresh, I1) = cv2.threshold(I1, 128, 255, cv2.THRESH_BINARY)
    (thresh, I2) = cv2.threshold(I2, 128, 255, cv2.THRESH_BINARY)

    I1=I1//255
    I2=I2//255


    #I1=I1//255
    #I2=I2//255
     
    Iblank = cv2.imread("blk.bmp", cv2.IMREAD_GRAYSCALE)
    (thresh, Iblank) = cv2.threshold(Iblank, 128, 255, cv2.THRESH_BINARY)

    stack =  Iblank[0:rows1,0:cols1]  ##np.zeros((rows*2,cols*2), dtype=[('x', 'int'), ('y', 'int')])


    #~~~~~~~~~~~~~~~~~~~
    #Stack the Images
    #~~~~~~~~~~~~~~~~~~~

    for i in range(rows1):
        for j in range(cols1):
     
            val1= I1[i][j] ^ I2[i][j]

            ##print(I1[i][j], I2[i][j],val1)
            
            stack[i][j]= val1

    stack1=stack*255

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    cv2.imwrite(signfile,stack1);
     


    os.remove(sh1fname)

    mes1="Shares Generated , \ncopy "+sh1fname+" \n in Cutomer Device "
    messagebox.showinfo("Result",mes1,icon=messagebox.INFO)




