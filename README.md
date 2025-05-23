# Chat da Torcida FURIA – Experiência Conversacional

Este projeto foi desenvolvido como parte do **Challenge #1: Experiência Conversacional** do processo seletivo da **FURIA Tech**.

🔗 Repositório oficial: https://github.com/Jmigliatti/telegram-bot-furia  
🔗 Link da Aplicação: https://projeto-furia.onrender.com

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

## 🧩 Estrutura do Projeto

- **Backend (`serve_webapp.py`)**  
  Toda a lógica de backend foi implementada com **Flask**, incluindo:
  - Configuração das **rotas HTTP**
  - Manipulação de **eventos WebSocket** com **Flask-SocketIO**
  - Comunicação com o **banco de dados PostgreSQL**
  - Camadas de autenticação, registro e controle de status dos usuários

- **Frontend (`/templates` e `/static`)**  
  A interface do usuário foi desenvolvida com:
  - **HTML + CSS** (na pasta `/templates`) para a estrutura das páginas
  -  e arquivos .png (na pasta `/static`) para o conteúdo visual da aplicação

- **Containerização (`Dockerfile`)**  
  O projeto inclui um `Dockerfile` configurado para criar um container compatível com o **Render**, a plataforma usada para **hospedar a aplicação online**.
  
---

## 🧪 Execução local

Você pode testar a aplicação localmente com Docker:

```bash
git clone https://github.com/Jmigliatti/telegram-bot-furia.git
cd telegram-bot-furia
docker compose up --build
```
---

## 📸 Galeria

Aqui você pode adicionar capturas de tela da aplicação em uso:

### 💬 Chat da Torcida
![Chat da Torcida](https://github.com/Jmigliatti/projeto-furia/blob/main/webapp/static/Captura%20de%20tela%202025-05-04%20185828.png)

### 🗓 Calendário de Jogos
![Calendário de Jogos](https://github.com/Jmigliatti/projeto-furia/blob/main/webapp/static/Captura%20de%20tela%202025-05-04%20185923.png)

### 📰 Feed de Acontecimentos
![Feed de Acontecimentos](https://github.com/Jmigliatti/projeto-furia/blob/main/webapp/static/Captura%20de%20tela%202025-05-04%20185858.png)

### Card do Feed
![Card do Feed](https://github.com/Jmigliatti/projeto-furia/blob/main/webapp/static/Captura%20de%20tela%202025-05-04%20191345.png)


---

## 🎥 Demonstração em vídeo

Assista à apresentação completa do projeto:

📺 [Clique aqui para ver o vídeo no YouTube](https://www.youtube.com/watch?v=SEU_LINK_AQUI)
