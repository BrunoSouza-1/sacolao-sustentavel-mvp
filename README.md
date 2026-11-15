# 🥬 Sacolão Sustentável — MVP

Plataforma web *mobile-first* desenvolvida para apoiar pequenos sacolões e hortifrútis de bairro na liquidação rápida de lotes perecíveis via WhatsApp, contribuindo diretamente para a **Meta 12.3 do ODS 12** (redução do desperdício de alimentos no varejo).

## 🚀 Arquitetura e Stack Tecnológica
- **Padrão Arquitetural:** Monolítico em Camadas (MVT — Model-View-Template)
- **Linguagem & Framework:** Python 3.12 + Flask 3.0
- **Persistência (ORM):** Flask-SQLAlchemy (SQLite local / PostgreSQL 16 em produção)
- **Interface & Acessibilidade:** HTML5 + Bootstrap 5 (WCAG 2.1 AA, áreas de toque ≥ 48px, alto contraste)
- **Segurança:** Autenticação com hash robusto (`PBKDF2-HMAC-SHA256`), consultas parametrizadas e escape automático XSS (Jinja2)

## 📂 Estrutura Prevista do Projeto
```text
sacolao-sustentavel-mvp/
├── app/
│   ├── models.py       # Entidades Lojista e Oferta
│   ├── routes.py       # Rotas públicas, painel administrativo e regras de negócio
│   └── templates/      # Interfaces HTML responsivas e acessíveis
├── tests/              # Testes automatizados unitários e de integração (pytest)
├── .github/workflows/  # Pipeline de Integração Contínua (CI)
├── requirements.txt    # Dependências do projeto
└── run.py              # Ponto de entrada da aplicação
