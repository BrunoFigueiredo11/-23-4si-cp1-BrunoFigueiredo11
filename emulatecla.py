#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv que emula precionamento de teclas

import cv2
import os,sys, os.path
import numpy as np
import math

#importes para emular precionamento de teclas
from pynput.keyboard import Key, Controller
import pynput
import time
import random

# keys = [
#     #Key.up,                                 # UP
#     #Key.down,                               # DOWN
#     #Key.left,                               # LEFT
#     #Key.right,                              # RIGHT
#     pynput.keyboard.KeyCode.from_char('S'),  # A
#     pynput.keyboard.KeyCode.from_char('W'),  # B
#     pynput.keyboard.KeyCode.from_char('a'),  # X
#     #Key.enter,                              # START
#     #Key.shift_r,                            # SELECT
# ]



# #Inicializa o controle 
# keyboard = Controller()




def filtro_de_cor(img_bgr, low_hsv, high_hsv):
    """ retorna a imagem filtrada"""
    img = cv2.cvtColor(img_bgr,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low_hsv, high_hsv)
    return mask 

def mascara_or(mask1, mask2,mask3,mask4):

     mask = cv2.bitwise_or(mask1,mask2)
     mask = cv2.bitwise_or(mask,mask3)
     mask = cv2.bitwise_or(mask,mask4)
     
     return mask

def desenha_cruz(img, cX,cY, size, color):
     """ faz a cruz no ponto cx cy"""
     cv2.line(img,(cX - size,cY),(cX + size,cY),color,5)
     cv2.line(img,(cX,cY - size),(cX, cY + size),color,5)    

def escreve_texto(img, text, origem, color):
     """ faz a cruz no ponto cx cy"""
 
     font = cv2.FONT_HERSHEY_SIMPLEX     
     cv2.putText(img, str(text), origem, font,1,color,2,cv2.LINE_AA)



def image_da_webcam(img):
 
    mask_hsv1 = filtro_de_cor(img, np.array([140, 130, 100])  , np.array([180, 255, 255])) #rosa
    mask_hsv2 = filtro_de_cor(img, np.array([18, 60,90]) , np.array([102, 255, 255]))#amarelo OK
    mask_hsv3 = filtro_de_cor(img, np.array([18, 80, 130])  , np.array([40, 255, 255]))#Mostarda
    mask_hsv4 = filtro_de_cor(img, np.array([80, 200, 180])  , np.array([180, 255, 255])) #rosa
    
    mask_hsv = mascara_or(mask_hsv1, mask_hsv2,mask_hsv3,mask_hsv4)

    contornos, _ = cv2.findContours(mask_hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    
    mask_rgb = cv2.cvtColor(mask_hsv, cv2.COLOR_GRAY2RGB) 
    contornos_img = mask_rgb.copy()
    
    maior = None
    maior_area = 0
    maior2_area = 0
    maior2 = None
    listArea = []
    for i in range (len(contornos)):
     listArea.append(contornos[i])
    for c in range (2):                
       listArea.sort(key=lambda listArea: cv2.contourArea(listArea),reverse=True)
       maior_area = int(cv2.contourArea(listArea[0]))
       maior= listArea[0]
       maior2_area = int(cv2.contourArea(listArea[1]))
       maior2= listArea[1]
    
 
    M = cv2.moments(maior)
    M2 = cv2.moments(maior2)

    # Verifica se existe alguma para calcular, se sim calcula e exibe no display
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cX2 = int(M2["m10"] / M2["m00"])
        cY2= int(M2["m01"] / M2["m00"])
        cv2.drawContours(contornos_img, [maior], -1, [255, 0, 0], 5)
        cv2.drawContours(contornos_img, [maior2], -1, [255, 0, 0], 5)
        cv2.line(contornos_img, (cX, cY), (cX2,cY2 ), (40, 255, 0), 5)
        #faz a cruz no centro de massa
        desenha_cruz(contornos_img, cX,cY, 20, (0,0,255))
        desenha_cruz(contornos_img, cX2,cY2, 20, (0,0,255))

        escreve_texto(contornos_img, maior_area, ((cX-50),(cY-100)), (50,255,0)) #maior area - informa o valor da area
        escreve_texto(contornos_img, maior2_area, ((cX2-50),(cY2-100)), (50,255,0)) #maior area - informa o valor da area

        font = cv2.FONT_HERSHEY_SIMPLEX
        angulo= ((cY-cY2)/(cX-cX2))
        value=math.degrees(math.atan(angulo))
        text=str(int(value*-1))
        cv2.putText(contornos_img, str(text+'Graus'), (cY+40,cX), font,1,(0,0,254),2,cv2.LINE_AA)
            
    else:
    # se não existe nada para segmentar
        cX, cY = 0, 0
        # Para escrever vamos definir uma fonte 
        texto = ' '
        origem = (0,50)
        escreve_texto(contornos_img, texto, origem, (0,0,255))
    


    return contornos_img

cv2.namedWindow("preview")
# define a entrada de video para webcam
#vc = cv2.VideoCapture(0)

vc = cv2.VideoCapture("video.mp4") # para ler um video mp4 

#configura o tamanho da janela 
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 540)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 380)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    img = image_da_webcam(frame) # passa o frame para a função imagem_da_webcam e recebe em img imagem tratada


    cv2.imshow("original", frame)
    cv2.imshow("preview", img)
   
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

cv2.destroyWindow("preview")
vc.release()
