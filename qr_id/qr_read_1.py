# does work due  missing lib: zbar
from qrtools import qrtools
qr = qrtools.QR()



myCode = qrtools.QR(filename="output.png")
if myCode.decode():
  print(myCode.data)
  print(myCode.data_type)
  print(myCode.data_to_string())
