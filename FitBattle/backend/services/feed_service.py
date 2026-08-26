from repositories.postagem_repository import PostagemRepository
from repositories.treino_repository import TreinoRepository


class FeedService:
    @staticmethod
    def _treino_para_card(treino):
        return {
            "id": f"treino-{treino.id}",
            "tipo": "treino",
            "usuarioId": treino.usuario_id,
            "usuarioNome": treino.autor.nome,
            "usuarioAvatar": treino.autor.avatar,
            "categoria": treino.categoria,
            "titulo": treino.titulo,
            "grupo": treino.grupo,
            "descricao": treino.descricao,
            "estatisticas": [
                {"valor": treino.duracao_min, "unidade": "min", "rotulo": "Duração"},
                {
                    "valor": treino.metrica2_valor,
                    "unidade": treino.metrica2_unidade,
                    "rotulo": treino.metrica2_rotulo,
                },
                {
                    "valor": treino.metrica3_valor,
                    "unidade": treino.metrica3_unidade,
                    "rotulo": treino.metrica3_rotulo,
                },
            ],
            "foto": None,
            "criadoEm": treino.criado_em.isoformat(),
        }

    @staticmethod
    def _postagem_para_card(postagem):
        return {
            "id": f"postagem-{postagem.id}",
            "tipo": "postagem",
            "usuarioId": postagem.usuario_id,
            "usuarioNome": postagem.autor.nome,
            "usuarioAvatar": postagem.autor.avatar,
            "descricao": postagem.texto,
            "estatisticas": [],
            "foto": postagem.foto,
            "criadoEm": postagem.criado_em.isoformat(),
        }

    @staticmethod
    def montar_feed(busca=None):
        cards = [FeedService._treino_para_card(t) for t in TreinoRepository.listar_todos()]
        cards += [FeedService._postagem_para_card(p) for p in PostagemRepository.listar_todas()]
        cards.sort(key=lambda c: c["criadoEm"], reverse=True)

        if busca:
            busca = busca.strip().lower()
            cards = [
                c
                for c in cards
                if busca in " ".join(
                    str(v) for v in (c.get("titulo"), c.get("grupo"), c["descricao"], c["usuarioNome"])
                    if v
                ).lower()
            ]

        return cards
