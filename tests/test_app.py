import pytest
from app import create_app, db
from app.models import Lojista, Oferta

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        lojista = Lojista(
            nome='Carlos Silva',
            email='carlos@sacolao.com',
            whatsapp_comercial='5511999999999'
        )
        lojista.set_senha('SenhaForte123')
        db.session.add(lojista)
        db.session.commit()

    with app.test_client() as client:
        yield client

def test_hash_senha_seguro():
    lojista = Lojista(nome='Teste', email='t@t.com', whatsapp_comercial='5511988887777')
    lojista.set_senha('MinhaSenha2026')
    assert lojista.senha_hash != 'MinhaSenha2026'
    assert lojista.senha_hash.startswith('pbkdf2:sha256')
    assert lojista.check_senha('MinhaSenha2026') is True

def test_bloqueio_acesso_nao_autenticado(client):
    resp = client.get('/painel')
    assert resp.status_code == 302

def test_fluxo_completo_oferta_e_catalogo(client):
    client.post('/login', data={'email': 'carlos@sacolao.com', 'senha': 'SenhaForte123'})
    resp = client.post('/painel', data={
        'nome_item': 'Tomate Italiano 3kg',
        'quantidade': '4 caixas',
        'preco_original': '18.00',
        'preco_promocional': '9.50'
    }, follow_redirects=True)
    assert b'publicada com sucesso' in resp.data

    vitrine = client.get('/')
    assert b'Tomate Italiano 3kg' in vitrine.data
    assert b'wa.me/5511999999999' in vitrine.data

def test_validacao_preco_promocional_invalido(client):
    client.post('/login', data={'email': 'carlos@sacolao.com', 'senha': 'SenhaForte123'})
    resp = client.post('/painel', data={
        'nome_item': 'Laranja Pera',
        'quantidade': '2 sacos',
        'preco_original': '10.00',
        'preco_promocional': '12.00'
    }, follow_redirects=True)
    assert b'deve ser menor que o pre' in resp.data