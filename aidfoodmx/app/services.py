from .models import Beneficiary


# Lista temporal para almacenar los beneficiarios
beneficiaries = []

# Servicio para registrar un beneficiario
def register_beneficiary_service(data):
    new_beneficiary = Beneficiary(
        id=len(beneficiaries) + 1,
        name=data.get('name'),
        satisfaction=data.get('satisfaction', 0)
    )
    beneficiaries.append(new_beneficiary)
    return new_beneficiary

# Servicio para obtener beneficiarios
def get_beneficiaries_service():
    return [{"id": b.id, "satisfaction": b.satisfaction} for b in beneficiaries]
