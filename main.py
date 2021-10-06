import os
import cv2
from model import evaluate, HES_Model

if __name__ == '__main__':
    images = []
    for i in os.listdir(os.getcwd()+'\\Images'):
        img = cv2.imread(os.getcwd()+'\\Images\\'+i)
        images.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

    print('Initializing model ....')
    H = HES_Model()
    print('Model initialized! Taking predictions ...')
    equation = H.predict_equation(images)
    print('Evaluating ..')
    evaluation = evaluate(equation)
    print('Equation :', equation+'\nEvaluation :', evaluation)
