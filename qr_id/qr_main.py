# crear un QR
import qrcode
img = qrcode.make("Feliz noche!")
f = open("output.png", "wb")
img.save(f)
f.close()
