import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-sacolao-2026')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///sacolao.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
with app.app_context():
        db.create_all()
        if not test_config:
            from .models import Lojista, Oferta
            if not Lojista.query.first():
                lojista = Lojista(
                    nome="Sacolão Verde Vida",
                    email="lojista@sacolao.com",
                    whatsapp_comercial="5511999999999"
                )
                lojista.set_senha("123456")
                db.session.add(lojista)
                db.session.commit()

                ofertas_iniciais = [
                    Oferta(
                        nome_item="Caixa de Tomates Orgânicos Maduros (2kg)",
                        quantidade="8",
                        preco_original=14.00,
                        preco_promocional=6.00,
                        lojista_id=lojista.id
                    ),
                    Oferta(
                        nome_item="Cacho de Banana Prata (1,5kg)",
                        quantidade="12",
                        preco_original=9.50,
                        preco_promocional=4.00,
                        lojista_id=lojista.id
                    ),
                    Oferta(
                        nome_item="Kit Folhosas Frescas (Alface + Couve)",
                        quantidade="6",
                        preco_original=8.00,
                        preco_promocional=3.50,
                        lojista_id=lojista.id
                    ),
                ]
                db.session.add_all(ofertas_iniciais)
                db.session.commit()

return app