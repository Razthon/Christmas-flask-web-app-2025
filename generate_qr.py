import qrcode

SITE_URL = "http://192.168.68.85:8080"


img = qrcode.make(SITE_URL)
img.save("site_qr.png")

print("QR code generated: site_qr.png")