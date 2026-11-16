from urllib.parse import quote
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from . import db
from .models import Lojista, Oferta

main_bp = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'lojista_id' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated

@main_bp.route('/')
def catalogo():
    ofertas_ativas = Oferta.query.filter_by(status='ativo').all()
    cards = []
    for o in ofertas_ativas:
        msg = f"Olá! Gostaria de reservar a oferta: {o.nome_item} ({o.quantidade}) por R$ {o.preco_promocional:.2f}."
        link_wpp = f"https://wa.me/{o.lojista.whatsapp_comercial}?text={quote(msg)}"
        cards.append({'oferta': o, 'link_wpp': link_wpp})
    return render_template('catalogo.html', cards=cards)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')
        lojista = Lojista.query.filter_by(email=email, ativo=True).first()
        if lojista and lojista.check_senha(senha):
            session['lojista_id'] = lojista.id
            return redirect(url_for('main.painel'))
        flash('Credenciais inválidas. Verifique e tente novamente.', 'danger')
    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.catalogo'))

@main_bp.route('/painel', methods=['GET', 'POST'])
@login_required
def painel():
    if request.method == 'POST':
        nome_item = request.form.get('nome_item', '').strip()
        quantidade = request.form.get('quantidade', '').strip()
        try:
            preco_orig = float(request.form.get('preco_original', '0').replace(',', '.'))
            preco_promo = float(request.form.get('preco_promocional', '0').replace(',', '.'))
        except ValueError:
            flash('Informe valores numéricos válidos para os preços.', 'danger')
            return redirect(url_for('main.painel'))

        if not nome_item or not quantidade or preco_orig <= 0 or preco_promo <= 0:
            flash('Todos os campos são obrigatórios e os preços devem ser maiores que zero.', 'danger')
            return redirect(url_for('main.painel'))

        if preco_promo >= preco_orig:
            flash('Erro: O preço promocional deve ser menor que o preço normal.', 'danger')
            return redirect(url_for('main.painel'))

        nova = Oferta(
            nome_item=nome_item,
            quantidade=quantidade,
            preco_original=preco_orig,
            preco_promocional=preco_promo,
            lojista_id=session['lojista_id']
        )
        db.session.add(nova)
        db.session.commit()
        flash(f'Oferta "{nome_item}" publicada com sucesso!', 'success')
        return redirect(url_for('main.painel'))

    ofertas = Oferta.query.filter_by(lojista_id=session['lojista_id']).order_by(Oferta.id.desc()).all()
    return render_template('painel.html', ofertas=ofertas)

@main_bp.route('/oferta/<int:oferta_id>/esgotar', methods=['POST'])
@login_required
def esgotar_oferta(oferta_id):
    oferta = db.get_or_404(Oferta, oferta_id)
    if oferta.lojista_id == session['lojista_id']:
        oferta.status = 'esgotado'
        db.session.commit()
        flash(f'Oferta "{oferta.nome_item}" marcada como esgotada.', 'info')
    return redirect(url_for('main.painel'))