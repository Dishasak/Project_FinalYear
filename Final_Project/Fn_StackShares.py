import cv2
import random
import numpy as np

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def my_filebrowser():
    root = tk.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    imgfile = filedialog.askopenfilename(initialdir = "testing",title = "Select Image",filetypes = (("Img files","*.*"),("all files","*.*")))
    root.destroy()
    return imgfile

def StackShares(accno):

    file_name = my_filebrowser()
    
    print(file_name)

    tok=file_name.split('/')
    print(tok)

    share1 = tok[-1]  

    share2 = accno+'_share2.bmp';

    print("Selected from "+file_name)

    I1 = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE);

    try:
        info1=I1.shape
        rows1, cols1 = (info1[0], info1[1])

        I2 = cv2.imread(share2, cv2.IMREAD_GRAYSCALE);
        info2=I2.shape
        rows2, cols2 = (info2[0], info2[1])

        cv2.imshow('Share 1',I1)

        cv2.imshow('Share 2',I2)


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

        print(stack)

        cv2.imshow('Staked',stack * 255);

        stack1=stack*255

        original=accno+".bmp"

        #compare stacked and original
        Oimg = cv2.imread(original, cv2.IMREAD_GRAYSCALE);

        diff = cv2.subtract(Oimg, stack1)


        print(sum(sum(diff)))
        if (sum(sum(diff))==0):
            ##messagebox.showinfo("Result","KYC Varified",icon=messagebox.INFO)
            res=1
        else:
            #messagebox.showinfo("Result","KYC NOT Varified",icon=messagebox.INFO)
            res=0
            
    except:

        #messagebox.showinfo("Result","KYC NOT Varified",icon=messagebox.INFO)
        res=0

    return res

        














