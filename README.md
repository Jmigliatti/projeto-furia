# Chat da Torcida FURIA – Experiência Conversacional

Este projeto foi desenvolvido como parte do **Challenge #1: Experiência Conversacional** do processo seletivo da **FURIA Tech**.

🔗 Repositório oficial: [https://github.com/Jmigliatti/telegram-bot-furia]([https://github.com/Jmigliatti/telegram-bot-furia](https://github.com/Jmigliatti/projeto-furia/))

---

## 🧠 Sobre o projeto

Criei um **protótipo web interativo** que simula a experiência de um fã acompanhando o time de **CS:GO da FURIA**, com foco na **interação, engajamento e usabilidade**.

O sistema é composto por:

- 💬 **Chat da torcida**: simula uma conversa entre fãs durante os jogos.
- 🗓 **Calendário de jogos**: acompanhe a agenda da FURIA.
- 📰 **Feed de acontecimentos**: últimas notícias, destaques de partidas e movimentações do time.
- 🤖 **Link direto para o Assistente Inteligente da FURIA no WhatsApp**: [Clique aqui](https://wa.me/5511993404466)

---

## 🚀 Tecnologias utilizadas

- 🐍 **Flask** – estrutura web do backend (arquivo principal: `serve_webapp.py`)
- 🖼 **HTML/CSS** – templates localizados na pasta `templates/` para o frontend
- 🐘 **PostgreSQL** – banco de dados utilizado via Render
- ☁️ **Render** – plataforma usada para hospedar o backend + frontend + banco de dados

---

## 🧪 Execução local

Você pode testar a aplicação localmente com Docker:

```bash
git clone https://github.com/Jmigliatti/telegram-bot-furia.git
cd telegram-bot-furia
docker compose up --build
