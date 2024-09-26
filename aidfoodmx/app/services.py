from .models import Beneficiary
from datetime import datetime
from collections import defaultdict

# Lista temporal para almacenar los beneficiarios
beneficiaries = []

# Servicio para registrar un beneficiario con fecha
def register_beneficiary_with_date(data):
    new_beneficiary = Beneficiary(
        id=len(beneficiaries) + 1,
        name=data.get('name'),
        satisfaction=data.get('satisfaction', 0),
        date_registered=datetime.strptime(data.get('date'), '%Y-%m-%d')  # Recibimos la fecha del body del request
    )
    beneficiaries.append(new_beneficiary)
    return new_beneficiary

# Servicio para obtener el número de beneficiarios por mes
def get_beneficiaries_per_month():
    count_per_month = defaultdict(int)
    for beneficiary in beneficiaries:
        month = beneficiary.date_registered.strftime('%Y-%m')  # Formato YYYY-MM
        count_per_month[month] += 1
    return count_per_month

# Servicio para obtener el número de beneficiarios por día en el mes actual
def get_beneficiaries_per_day():
    current_month = datetime.now().strftime('%Y-%m')
    count_per_day = defaultdict(int)
    for beneficiary in beneficiaries:
        month = beneficiary.date_registered.strftime('%Y-%m')
        if month == current_month:
            day = beneficiary.date_registered.strftime('%Y-%m-%d')
            count_per_day[day] += 1
    return count_per_day
