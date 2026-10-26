# app/__init__.py
# ... dentro de create_app ...
app.config.from_object(config_class)
app.config["SQLALCHEMY_DATABASE_URI"] = config_class.build_uri()
    
# Inicializar Cloudinary si las variables existen
config_class.init_cloudinary()