# ==========================================================
# ENTIDADES DEL SISTEMA
# ==========================================================

from dataclasses import dataclass


@dataclass
class Candidato:
    """
    Representa a un candidato dentro de Worker Location.
    """

    id_candidato: int
    nombre: str
    profesion: str
    experiencia: int
    habilidades: str