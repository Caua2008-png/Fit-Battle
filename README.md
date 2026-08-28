# Fit-Battle

Projeto desenvolvido por Bernardo Nardelli, Cauã Gomes, João Paulo Costa, João Pedro Braga, Miguel Assunção e Henrique Vale.

A ideia do Fit-Battle nasceu de uma vontade simples: tornar o treino menos solitário. É uma rede social voltada pra quem treina — você cria uma conta, monta seu perfil, registra seus treinos e posts, ganha XP e sobe de nível conforme mantém a consistência, e ainda pode ver como está no ranking em relação aos outros usuários. A ideia é misturar um pouco de jogo com hábito saudável.

Por baixo dos panos, o backend é feito em Flask com SQLAlchemy, e o frontend é HTML, CSS e JavaScript puro (sem framework), servido diretamente pelo Flask — nada de build complicado, é só rodar e usar.

## Como o projeto está organizado

```
FitBattle/
├── frontend/
│   ├── index.html      # Tela de cadastro
│   ├── login.html      # Tela de login
│   ├── app.html         # O app em si (perfil + feed), depois de logado
│   ├── style.css        # Estilo das telas de cadastro/login
│   ├── app.css           # Estilo do app
│   ├── script.js         # Lógica da tela de cadastro
│   ├── login.js            # Lógica da tela de login
│   └── app.js                # Lógica do app, consome a API do backend
└── backend/
    ├── app.py             # Onde o Flask app é criado, registra as rotas e serve o frontend
    ├── requirements.txt
    ├── database/          # Instância do SQLAlchemy
    ├── models/            # Usuario, Treino, Postagem
    ├── repositories/       # Acesso ao banco de dados
    ├── services/            # Regras de negócio (validações, cálculo de XP, nível, streak)
    ├── controllers/          # Camada HTTP: recebe a request, chama o service, devolve o JSON
    ├── routers/                # Registro das rotas da API (blueprint /api)
    └── static/uploads/          # Fotos de perfil e de postagens que os usuários enviam
```

## Rodando o projeto na sua máquina

Só precisa de Python instalado. No PowerShell, dentro da pasta do projeto:

```powershell
cd FitBattle\backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python app.py
```

Depois é só abrir `http://127.0.0.1:5000/` no navegador e criar sua conta. Na primeira vez que você roda, o banco SQLite (`fitbattle.db`) é criado sozinho, então não precisa se preocupar em configurar nada além disso.

## O que dá pra fazer no app

- Criar conta e fazer login (a sessão fica salva em cookie, e a senha nunca é guardada em texto puro, sempre com hash)
- Editar o perfil: nome, usuário, localização, bio, peso, altura, idade e foto
- Publicar treinos (musculação, cardio, yoga ou outro tipo) e postagens com foto
- Ver o feed com busca, apagar seu próprio conteúdo e compartilhar o link de um post
- Acompanhar XP, nível e sequência de dias treinando (streak), tudo calculado automaticamente
- Conferir o ranking dos usuários por XP
- Ajustar configurações, como unidade de peso, notificações e visibilidade no ranking

## API

Todas as rotas ficam sob o prefixo `/api`:

| Método | Rota | O que faz |
|---|---|---|
| POST | `/cadastro` | Cria um usuário novo e já loga ele |
| POST | `/login` | Loga com usuário ou email + senha |
| POST | `/logout` | Encerra a sessão |
| GET | `/sessao` | Checa se tem alguém logado |
| GET/PUT | `/perfil` | Lê ou atualiza o perfil de quem está logado |
| POST | `/perfil/avatar` | Envia a foto de perfil |
| PUT | `/perfil/configuracoes` | Atualiza as configurações do usuário |
| GET | `/ranking` | Lista o ranking por XP |
| GET | `/feed` | Lista os treinos e postagens (aceita `?busca=` pra filtrar) |
| POST | `/treinos` | Publica um treino |
| POST | `/postagens` | Publica uma postagem (pode incluir foto) |
| DELETE | `/cards/<tipo>/<id>` | Apaga um treino ou postagem que seja seu |
