import qrcode


def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create QR code image
    img = qr.make_image(fill='black', back_color='white')
    img.save("../static/images/qrcode.png")


if __name__ == "__main__":
    generate_qr_code("http://127.0.0.1:5000/login")
