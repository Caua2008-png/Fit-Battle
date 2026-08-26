import os
import uuid

from werkzeug.utils import secure_filename

from models.postagem import Postagem
from repositories.postagem_repository import PostagemRepository
from repositories.usuario_repository import UsuarioRepository
from services.constantes import XP_POSTAGEM
from services.usuario_service import UsuarioService

EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "webp"}


class PostagemService:
    @staticmethod
    def cadastrar(usuario, texto, arquivo_foto, pasta_upload):
        texto = (texto or "").strip()
        if not texto:
            raise ValueError("Escreva algo para publicar.")

        caminho_foto = None
        if arquivo_foto and arquivo_foto.filename:
            extensao = (
                arquivo_foto.filename.rsplit(".", 1)[-1].lower()
                if "." in arquivo_foto.filename
                else ""
            )
            if extensao not in EXTENSOES_PERMITIDAS:
                raise ValueError("Formato de imagem não suportado.")
            nome_arquivo = secure_filename(f"{uuid.uuid4().hex}.{extensao}")
            os.makedirs(pasta_upload, exist_ok=True)
            arquivo_foto.save(os.path.join(pasta_upload, nome_arquivo))
            caminho_foto = f"/static/uploads/{nome_arquivo}"

        postagem = Postagem(usuario_id=usuario.id, texto=texto, foto=caminho_foto)
        PostagemRepository.salvar(postagem)

        UsuarioService.adicionar_xp(usuario, XP_POSTAGEM)
        UsuarioRepository.atualizar()
        return postagem

    @staticmethod
    def excluir(usuario, postagem_id):
        postagem = PostagemRepository.buscar_por_id(postagem_id)
        if not postagem:
            raise ValueError("Postagem não encontrada.")
        if postagem.usuario_id != usuario.id:
            raise PermissionError("Você não pode excluir uma postagem de outro usuário.")
        PostagemRepository.excluir(postagem)
