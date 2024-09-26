from .models import Beneficiary
from datetime import datetime
from collections import defaultdict 
from .models import FoodPackage


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




# Lista temporal para almacenar los paquetes de comida y sus rankings
food_packages = []

# Servicio para registrar un ranking de paquete de comida
def register_food_package_ranking(data):
    # Busca si el paquete ya existe por su ID
    package = next((p for p in food_packages if p.id == data['id']), None)
    
    if not package:
        # Si no existe, crea uno nuevo
        package = FoodPackage(
            id=data.get('id'),
            info=data.get('info'),
            satisfaction_scores=[],
            date_rated=datetime.strptime(data.get('date'), '%Y-%m-%d')
        )
        food_packages.append(package)
    
    # Agrega la calificación al paquete existente
    package.satisfaction_scores.append(data.get('satisfaction'))

    return package

# Servicio para obtener el promedio de satisfacción por paquete mes a mes
def get_food_package_rankings_per_month():
    rankings_per_month = defaultdict(lambda: defaultdict(list))

    for package in food_packages:
        # Obtener el mes en formato YYYY-MM
        month = package.date_rated.strftime('%Y-%m')
        # Agrega el promedio de satisfacción de cada paquete en ese mes
        avg_satisfaction = sum(package.satisfaction_scores) / len(package.satisfaction_scores)
        rankings_per_month[month][package.info].append(avg_satisfaction)

    # Prepara los datos para devolver el promedio por paquete en cada mes
    averages_per_month = {
        month: {
            package_info: sum(scores) / len(scores)
            for package_info, scores in packages.items()
        }
        for month, packages in rankings_per_month.items()
    }

    return averages_per_month