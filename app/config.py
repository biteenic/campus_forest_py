import cloudinary
import cloudinary.uploader
import cloudinary.api

class Config:
    # ... (tus configuraciones anteriores de BD y SECRET_KEY) ...
    
    # Configuración de Cloudinary (se llenará con variables de entorno en Render)
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

    @staticmethod
    def init_cloudinary():
        if os.getenv("CLOUDINARY_CLOUD_NAME"):
            cloudinary.config(
                cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
                api_key=os.getenv("CLOUDINARY_API_KEY"),
                api_secret=os.getenv("Cloudinary_API_SECRET"),
                secure=True
            )