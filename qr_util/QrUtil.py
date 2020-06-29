import qrcode;
import io;

class QrUtil:
    def __init__(self, version=1, tipo = qrcode.constants.ERROR_CORRECT_L, dimension = 10,borde = 4):
        self.qr_gen = qrcode.QRCode(
        version=version,
        error_correction=tipo,
        box_size=dimension,
        border=borde)

    def crear(self, mensaje, formato="PNG", toBytes=False):
        self.qr_gen.add_data(mensaje)
        self.qr_gen.make(fit=True)
        qr_img = self.qr_gen.make_image()
        if toBytes:
            img = io.BytesIO()
            qr_img.save(img, format=formato)
            img.seek(0)
            return img
        else:
            return qr_img
