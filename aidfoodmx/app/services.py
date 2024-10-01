from .models import Beneficiary
from datetime import datetime
from collections import defaultdict 
from .models import FoodPackage, Inventory
from datetime import datetime, timedelta
from collections import defaultdict
import math


# Lista temporal para almacenar los beneficiarios
beneficiaries = []

# Servicio para registrar un beneficiario con fecha
def register_beneficiary_with_region(data):
    new_beneficiary = Beneficiary(
        id=len(beneficiaries) + 1,
        name=data.get('name'),
        satisfaction=data.get('satisfaction', 0),
        date_registered=datetime.strptime(data.get('date'), '%Y-%m-%d'),
        region=data.get('region')  # Registrar la región
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


# Servicio para obtener las tendencias de beneficiarios por región
def get_beneficiary_trends_by_region(region, start_date, end_date):
    trends = defaultdict(int)

    for beneficiary in beneficiaries:
        if beneficiary.region == region:
            # Verificar si la fecha está dentro del rango
            if start_date <= beneficiary.date_registered <= end_date:
                month = beneficiary.date_registered.strftime('%Y-%m')
                trends[month] += 1
    
    return trends

# Servicio para predecir el número de beneficiarios en el futuro
def predict_future_beneficiaries(region, period):
    # Usamos el servicio anterior para obtener las tendencias pasadas
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    
    # Obtenemos los datos del último año
    trends = get_beneficiary_trends_by_region(region, one_year_ago, today)

    # Calcular el promedio de crecimiento mensual
    monthly_counts = list(trends.values())
    
    if len(monthly_counts) < 2:
        return {"error": "No hay suficientes datos históricos para predecir."}

    growth_rates = [
        (monthly_counts[i] - monthly_counts[i - 1]) / monthly_counts[i - 1]
        for i in range(1, len(monthly_counts))
        if monthly_counts[i - 1] > 0  # Evitar división por cero
    ]

    # Promedio de la tasa de crecimiento mensual
    avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0

    # Predicción para los próximos meses
    last_month_count = monthly_counts[-1]
    predictions = {}

    for i in range(1, period + 1):
        next_month = (today + timedelta(days=30 * i)).strftime('%Y-%m')
        last_month_count += math.ceil(last_month_count * avg_growth_rate)
        predictions[next_month] = last_month_count

    return predictions



# Initialize inventory with zero values
inventory = Inventory(non_perishables=0, cereals=0, fruits_vegetables=0, dairy=0, meat=0, last_updated=datetime.now())

# Donations history to track per month and per week
donations = defaultdict(lambda: defaultdict(int))  # {'2024-09': {'non_perishables': 10, 'cereals': 5, ...}}

# Servicio para actualizar inventario
def update_inventory(data):
    inventory.non_perishables += data.get('non_perishables', 0)
    inventory.cereals += data.get('cereals', 0)
    inventory.fruits_vegetables += data.get('fruits_vegetables', 0)
    inventory.dairy += data.get('dairy', 0)
    inventory.meat += data.get('meat', 0)
    inventory.last_updated = datetime.now()
    return inventory

# Servicio para registrar donaciones por semana y mes
def record_donations(data):
    today = datetime.now()
    month = today.strftime('%Y-%m')
    week = today.strftime('%Y-%U')  # Week number of the year

    # Actualizar la cantidad donada por mes y por semana
    donations[month]['non_perishables'] += data.get('non_perishables', 0)
    donations[month]['cereals'] += data.get('cereals', 0)
    donations[month]['fruits_vegetables'] += data.get('fruits_vegetables', 0)
    donations[month]['dairy'] += data.get('dairy', 0)
    donations[month]['meat'] += data.get('meat', 0)

    return donations[month]

# Servicio para obtener el inventario total actual
def get_total_inventory():
    return inventory

# Servicio para obtener las donaciones por mes
def get_donations_per_month():
    return donations

# Servicio para obtener las donaciones por semana
def get_donations_per_week():
    week_donations = defaultdict(lambda: defaultdict(int))
    for month, items in donations.items():
        for food_type, amount in items.items():
            week = datetime.strptime(month, '%Y-%m').strftime('%Y-%U')
            week_donations[week][food_type] += amount
    return week_donations
