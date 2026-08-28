# Fit-Battle

#Bernardo Nardelli, Cauã Gomes, João Paulo Costa, João Pedro Braga, Miguel Assunção, Henrique Vale.

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
|
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
    
        
Funcionalidades:
1:Cadastrar Usuarios
2:Atualizar o cadastro dos Usuarios
3:Excluir Usuarios
4:Buscar Usuarios
5:Consultar os IDs do Usuarios
6:Gera as estatisticas do Usuario
7:Salva o registro do Usuario
8:Lista os Usuarios
9:Valida os dados inseridos
