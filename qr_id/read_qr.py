#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 12:11:22 2018
@author: altaruru
"""

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

def tifrbar(tifname, txtname):
    try:
        # carga imagen
        tifimg = cv2.imread(tifname)
        # carga códigos de barras de la imagen en lista
        lstbc = pyzbar.decode(tifimg)
        # recorre objetos encontrados
        fptxt = open(txtname, 'w')
        for bc in lstbc:
            npoint = bc.polygon
            # estamos buscando un area rectangular, si hay más de 4 puntos intenta una aproximación
            if len(npoint) > 4 :
              hull = cv2.convexHull(np.array([point for point in npoint], dtype=np.float32))
              hull = list(map(tuple, np.squeeze(hull)))
            else :
              hull = npoint
            n = len(hull)
            if (n>0):
                # código válido
                slinea="%s|%s\n" % (bc.data, bc.type)
                print(slinea)
                fptxt.write(slinea)
        fptxt.closed
        return True
    except:
        # si hay algún error...
        print("ERROR de lectura, tifrbar")
    return False

def test():
    spathfile="output.png"
    spathtxt="output.txt"
    tifrbar(spathfile, spathtxt)

test()