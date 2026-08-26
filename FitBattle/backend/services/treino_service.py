from models.treino import Treino
from repositories.treino_repository import TreinoRepository
from repositories.usuario_repository import UsuarioRepository
from services.constantes import CATEGORIAS_TREINO, XP_TREINO
from services.usuario_service import UsuarioService


class TreinoService:
    @staticmethod
    def cadastrar(usuario, dados):
        categoria = dados.get("categoria")
        if categoria not in CATEGORIAS_TREINO:
            raise ValueError("Categoria de treino inválida.")

        grupo = (dados.get("grupo") or "").strip()
        descricao = (dados.get("descricao") or "").strip()
        if not grupo:
            raise ValueError("Informe o grupo/título do treino.")
        if not descricao:
            raise ValueError("Descreva como foi o treino.")

        try:
            duracao = float(dados.get("duracao"))
            metrica2 = float(dados.get("metrica2"))
            metrica3 = float(dados.get("metrica3"))
        except (TypeError, ValueError):
            raise ValueError("Preencha os valores numéricos do treino.")

        info = CATEGORIAS_TREINO[categoria]
        treino = Treino(
            usuario_id=usuario.id,
            categoria=categoria,
            titulo=info["titulo"],
            grupo=grupo.upper(),
            descricao=descricao,
            duracao_min=duracao,
            metrica2_valor=metrica2,
            metrica2_unidade=info["unidades"][1],
            metrica2_rotulo=info["rotulos"][1],
            metrica3_valor=metrica3,
            metrica3_unidade=info["unidades"][2],
            metrica3_rotulo=info["rotulos"][2],
        )
        TreinoRepository.salvar(treino)

        UsuarioService.adicionar_xp(usuario, XP_TREINO)
        UsuarioService.registrar_atividade_treino(usuario)
        UsuarioRepository.atualizar()
        return treino

    @staticmethod
    def excluir(usuario, treino_id):
        treino = TreinoRepository.buscar_por_id(treino_id)
        if not treino:
            raise ValueError("Treino não encontrado.")
        if treino.usuario_id != usuario.id:
            raise PermissionError("Você não pode excluir um treino de outro usuário.")
        TreinoRepository.excluir(treino)
