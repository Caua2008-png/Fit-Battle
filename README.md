# Fit-Battle

Bernardo Nardelli, Cauã Gomes, João Paulo Costa, João Pedro Braga, Miguel Assunção, Henrique Vale.

Rede social de treinos: cadastro/login, perfil com nível e XP, feed de treinos e postagens, ranking local e configurações. Backend em Flask + SQLAlchemy, frontend em HTML/CSS/JS puro servido pelo próprio Flask.

## Estrutura

```
FitBattle/
├── frontend/
│   ├── index.html      # Cadastro
│   ├── login.html       # Login
│   ├── app.html          # Aplicativo (perfil + feed), após autenticado
│   ├── style.css         # Estilo de cadastro/login
│   ├── app.css           # Estilo do aplicativo
│   ├── script.js         # Lógica de cadastro
│   ├── login.js           # Lógica de login
│   └── app.js              # Lógica do aplicativo (consome a API)
└── backend/
    ├── app.py             # Cria o Flask app, registra rotas e serve o frontend
    ├── requirements.txt
    ├── database/          # Instância do SQLAlchemy
    ├── models/            # Usuario, Treino, Postagem
    ├── repositories/       # Acesso ao banco
    ├── services/            # Regras de negócio (validação, XP, nível, streak)
    ├── controllers/          # Camada HTTP (recebe request, chama service, devolve JSON)
    ├── routers/                # Registro das rotas da API (blueprint /api)
    └── static/uploads/          # Fotos de perfil e de postagens enviadas
```

## Como rodar

```powershell
cd FitBattle\backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python app.py
```

Acesse `http://127.0.0.1:5000/` para se cadastrar. O banco SQLite (`fitbattle.db`) é criado automaticamente na primeira execução.

## Funcionalidades

1. Cadastro e login de usuários (sessão via cookie, senha com hash)
2. Edição de perfil (nome, usuário, localização, bio, peso, altura, idade, foto)
3. Publicação de treinos (musculação, cardio, yoga, outro) e postagens com foto
4. Feed com busca, exclusão de conteúdo próprio e compartilhamento de link
5. Cálculo automático de XP, nível e sequência (streak) de treinos
6. Ranking local dos usuários por XP
7. Configurações (unidade de peso, notificações, visibilidade no ranking)

## API (`/api`)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/cadastro` | Cria um usuário e já autentica |
| POST | `/login` | Autentica por usuário ou email + senha |
| POST | `/logout` | Encerra a sessão |
| GET | `/sessao` | Verifica se há sessão ativa |
| GET/PUT | `/perfil` | Lê/atualiza o perfil do usuário logado |
| POST | `/perfil/avatar` | Envia a foto de perfil |
| PUT | `/perfil/configuracoes` | Atualiza as configurações |
| GET | `/ranking` | Lista o ranking local por XP |
| GET | `/feed` | Lista treinos e postagens (aceita `?busca=`) |
| POST | `/treinos` | Publica um treino |
| POST | `/postagens` | Publica uma postagem (aceita foto) |
| DELETE | `/cards/<tipo>/<id>` | Exclui um treino ou postagem próprio |
