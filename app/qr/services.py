import qrcode
import cloudinary.uploader
from io import BytesIO
from flask import current_app
from ..extensions import db
from ..models import CodigoQR

def generar_qr_para_arbol(arbol):
    base = current_app.config["BASE_URL"].rstrip("/")
    url = f"{base}/arbol/ver/{arbol.codigo}"
    
    # Generar QR en memoria
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar en un buffer de memoria
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
    # Subir a Cloudinary
    nombre_archivo = f"qr_{arbol.codigo}"
    upload_result = cloudinary.uploader.upload(
        img_buffer,
        public_id=nombre_archivo,
        folder="sifu_qr_codes"
    )
    
    # La URL segura que devuelve Cloudinary
    url_qr_image = upload_result['secure_url']

    registro = CodigoQR.query.filter_by(arbol_id=arbol.id).first()
    if not registro:
        registro = CodigoQR(arbol_id=arbol.id, codigo=arbol.codigo, url=url, archivo_qr=url_qr_image)
        db.session.add(registro)
    else:
        registro.url = url
        registro.archivo_qr = url_qr_image
    
    db.session.commit()
    return registro