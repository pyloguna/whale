# doest work due missing lib
from qrtools import qrtools
qr = qrtools.QR()
qr.decode("output.png")
print(qr.data)