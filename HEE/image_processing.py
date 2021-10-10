import os
from tkinter import Tk, filedialog
import cv2


def get_user_image_path():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    PATH = filedialog.askopenfilename()
    root.destroy()
    root.mainloop()
    return PATH

def process_image(img_path):
    images = []

    for i in os.listdir(os.getcwd()+'/Images'):
        img = cv2.imread(os.getcwd()+'/Images/'+i)
        images.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    return images
