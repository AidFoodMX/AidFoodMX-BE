from dataclasses import dataclass
from datetime import datetime

@dataclass
class Beneficiary:
    id: int
    name: str
    satisfaction: int
    date_registered: datetime  # Nueva propiedad para almacenar la fecha de registro
