from dataclasses import dataclass
from datetime import datetime

@dataclass
class Beneficiary:
    id: int
    name: str
    satisfaction: int
    date_registered: datetime  # Nueva propiedad para almacenar la fecha de registro

@dataclass
class FoodPackage:
    id: int
    info: str  # Información del paquete de comida
    satisfaction_scores: list[int]  # Lista para almacenar los rankings
    date_rated: datetime  # Fecha en la que fue calificado