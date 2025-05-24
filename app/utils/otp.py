import pyotp
import qrcode
import io
import base64

def generate_otp_secret():
    return pyotp.random_base32()

def generate_qr_code(username, email, secret):
    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name=f"DashboardKPIs ({username})")
    qr = qrcode.make(otp_uri)
    
    buffered = io.BytesIO()
    qr.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_base64  # Puedes incrustarlo como: <img src="data:image/png;base64,{img_base64}">
