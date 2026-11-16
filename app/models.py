from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class Lojista(db.Model):
    __tablename__ = 'lojista'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    whatsapp_comercial = db.Column(db.String(20), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    ofertas = db.relationship('Oferta', backref='lojista', lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha, method='pbkdf2:sha256')

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Oferta(db.Model):
    __tablename__ = 'oferta'
    id = db.Column(db.Integer, primary_key=True)
    nome_item = db.Column(db.String(120), nullable=False)
    quantidade = db.Column(db.String(60), nullable=False)
    preco_original = db.Column(db.Float, nullable=False)
    preco_promocional = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='ativo')  # 'ativo' ou 'esgotado'
    lojista_id = db.Column(db.Integer, db.ForeignKey('lojista.id'), nullable=False)