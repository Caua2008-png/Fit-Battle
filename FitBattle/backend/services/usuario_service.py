import os
import re
import uuid
from datetime import date, timedelta

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from services.constantes import EMAIL_PATTERN, NIVEIS, XP_POR_NIVEL

EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "webp"}


class UsuarioService:
    @staticmethod
    def calcular_nivel(xp):
        indice = min(xp // XP_POR_NIVEL, len(NIVEIS) - 1)
        xp_no_nivel = xp - indice * XP_POR_NIVEL
        percentual = min(100, round((xp_no_nivel / XP_POR_NIVEL) * 100))
        restante = XP_POR_NIVEL - xp_no_nivel
        return {"nome": NIVEIS[int(indice)], "percentual": percentual, "restante": int(restante)}

    @staticmethod
    def cadastrar(dados):
        usuario = (dados.get("usuario") or "").strip()
        email = (dados.get("email") or "").strip().lower()
        senha = dados.get("senha") or ""
        confirma_senha = dados.get("confirmaSenha")

        if len(usuario) < 3:
            raise ValueError("Nome de usuário deve ter ao menos 3 caracteres.")
        if not re.match(EMAIL_PATTERN, email):
            raise ValueError("Informe um e-mail válido.")
        if len(senha) < 8:
            raise ValueError("A senha deve ter no mínimo 8 caracteres.")
        if confirma_senha is not None and senha != confirma_senha:
            raise ValueError("As senhas não coincidem.")
        if UsuarioRepository.buscar_por_usuario(usuario):
            raise ValueError("Nome de usuário já está em uso.")
        if UsuarioRepository.buscar_por_email(email):
            raise ValueError("E-mail já cadastrado no sistema.")

        novo_usuario = Usuario(
            usuario=usuario,
            email=email,
            senha_hash=generate_password_hash(senha),
            nome=usuario,
            handle="@" + usuario,
        )
        return UsuarioRepository.salvar(novo_usuario)

    @staticmethod
    def autenticar(identificador, senha):
        identificador = (identificador or "").strip()
        usuario = UsuarioRepository.buscar_por_usuario_ou_email(identificador)
        if not usuario or not check_password_hash(usuario.senha_hash, senha or ""):
            raise ValueError("Usuário ou senha inválidos.")
        return usuario

    @staticmethod
    def montar_perfil(usuario, total_treinos, total_postagens, posicao_ranking):
        nivel = UsuarioService.calcular_nivel(usuario.xp)
        return {
            "id": usuario.id,
            "usuario": usuario.usuario,
            "nome": usuario.nome,
            "handle": usuario.handle,
            "localizacao": usuario.localizacao,
            "bio": usuario.bio,
            "avatar": usuario.avatar,
            "peso": usuario.peso,
            "altura": usuario.altura,
            "idade": usuario.idade,
            "xp": usuario.xp,
            "streak": usuario.streak,
            "totalTreinos": total_treinos,
            "totalPostagens": total_postagens,
            "rankingPosicao": posicao_ranking,
            "nivel": nivel,
            "configuracoes": {
                "unitLb": usuario.unit_lb,
                "notif": usuario.notif,
                "publicRanking": usuario.public_ranking,
            },
        }

    @staticmethod
    def atualizar_perfil(usuario, dados):
        if dados.get("nome"):
            usuario.nome = dados["nome"].strip()
        if dados.get("handle"):
            usuario.handle = dados["handle"].strip()
        if dados.get("localizacao") is not None:
            usuario.localizacao = dados["localizacao"].strip()
        if dados.get("bio") is not None:
            usuario.bio = dados["bio"].strip()
        if dados.get("peso") not in (None, ""):
            usuario.peso = float(dados["peso"])
        if dados.get("altura") not in (None, ""):
            usuario.altura = float(dados["altura"])
        if dados.get("idade") not in (None, ""):
            usuario.idade = int(dados["idade"])
        UsuarioRepository.atualizar()
        return usuario

    @staticmethod
    def atualizar_configuracoes(usuario, dados):
        if "unitLb" in dados:
            usuario.unit_lb = bool(dados["unitLb"])
        if "notif" in dados:
            usuario.notif = bool(dados["notif"])
        if "publicRanking" in dados:
            usuario.public_ranking = bool(dados["publicRanking"])
        UsuarioRepository.atualizar()
        return usuario

    @staticmethod
    def salvar_avatar(usuario, arquivo, pasta_upload):
        extensao = arquivo.filename.rsplit(".", 1)[-1].lower() if "." in arquivo.filename else ""
        if extensao not in EXTENSOES_PERMITIDAS:
            raise ValueError("Formato de imagem não suportado.")

        nome_arquivo = secure_filename(f"{uuid.uuid4().hex}.{extensao}")
        os.makedirs(pasta_upload, exist_ok=True)
        arquivo.save(os.path.join(pasta_upload, nome_arquivo))

        usuario.avatar = f"/static/uploads/{nome_arquivo}"
        UsuarioRepository.atualizar()
        return usuario

    @staticmethod
    def registrar_atividade_treino(usuario):
        hoje = date.today()
        if usuario.ultimo_treino_em == hoje:
            pass
        elif usuario.ultimo_treino_em == hoje - timedelta(days=1):
            usuario.streak += 1
        else:
            usuario.streak = 1
        usuario.ultimo_treino_em = hoje

    @staticmethod
    def adicionar_xp(usuario, quantidade):
        usuario.xp += quantidade

    @staticmethod
    def posicao_no_ranking(usuario):
        usuarios = UsuarioRepository.listar_ranking()
        for indice, item in enumerate(usuarios):
            if item.id == usuario.id:
                return indice + 1
        return None

    @staticmethod
    def montar_ranking():
        usuarios = UsuarioRepository.listar_ranking()
        return [
            {
                "posicao": indice + 1,
                "id": item.id,
                "nome": item.nome,
                "avatar": item.avatar,
                "xp": item.xp,
            }
            for indice, item in enumerate(usuarios)
            if item.public_ranking
        ]
