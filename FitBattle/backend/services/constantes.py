EMAIL_PATTERN = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

XP_TREINO = 120
XP_POSTAGEM = 40
XP_POR_NIVEL = 1000
NIVEIS = ["iniciante", "intermediário", "avançado", "profissional", "elite"]

CATEGORIAS_TREINO = {
    "musculacao": {
        "titulo": "Musculação",
        "rotulos": ("Duração", "Carga MAX.", "Séries"),
        "unidades": ("min", "Kg", ""),
    },
    "cardio": {
        "titulo": "Cardio",
        "rotulos": ("Duração", "Velocidade", "Inclinação"),
        "unidades": ("min", "Km", ""),
    },
    "yoga": {
        "titulo": "Yoga",
        "rotulos": ("Duração", "Intensidade", "Séries"),
        "unidades": ("min", "", ""),
    },
    "outro": {
        "titulo": "Treino",
        "rotulos": ("Duração", "Carga MAX.", "Séries"),
        "unidades": ("min", "Kg", ""),
    },
}
