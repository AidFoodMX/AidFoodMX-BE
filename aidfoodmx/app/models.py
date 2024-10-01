from dataclasses import dataclass
from datetime import datetime

@dataclass
class Beneficiary:
    id: int
    name: str
    satisfaction: int
    date_registered: datetime
    region: str  # Nueva propiedad para la región Nueva propiedad para almacenar la fecha de registro

@dataclass
class FoodPackage:
    id: int
    info: str  # Información del paquete de comida
    satisfaction_scores: list[int]  # Lista para almacenar los rankings
    date_rated: datetime  # Fecha en la que fue calificado
    
    

    ## We are also expecting to create inventory management for the food packages. 
    
@dataclass
class Inventory:
    non_perishables: int
    cereals: int
    fruits_vegetables: int
    dairy: int
    meat: int
    last_updated: datetime  # Keep track of when the inventory was last updated