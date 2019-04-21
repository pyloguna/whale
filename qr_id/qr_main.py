# crear un QR
# wrapper for qrcode. QR image generator

import qrcode
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

class QrInterfase:

    def __int__(self):
        pass

    def create_qr_image_file(self, message="foo", filename="output.png"):
        img = qrcode.make(message)
        with open(filename, "wb") as f:
            img.save(f)

    def read_qr(self, tifname, txtname):
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

if __name__ == "__main__":
    qr_obj =QrInterfase()
    qr_obj.create_qr_image_file(message='hello', filename='hello.png')
    qr_obj.read_qr(tifname='hello.png', txtname='hello.txt')
