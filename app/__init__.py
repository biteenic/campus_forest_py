# app/__init__.py

import os
import logging
from flask import Flask
from .config import Config
from .extensions import db, login_manager, csrf

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Asignar URI construida dinámicamente
    app.config["SQLALCHEMY_DATABASE_URI"] = config_class.build_uri()

    
    # Inicializar Cloudinary si las variables existen
    config_class.init_cloudinary()

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Cargar usuario
    from .models import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # Validar conexión al iniciar
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                conn.execute(db.text("SELECT 1"))
            app.logger.info("✅ Conexión exitosa a TiDB Cloud")
        except Exception as e:
            app.logger.error("❌ Error conectando a TiDB Cloud: %s", e)
            raise

    return app