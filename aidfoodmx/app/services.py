from datetime import datetime, timedelta
from collections import defaultdict
import math
from supabase_client import supabase
from .models import Beneficiary, FoodPackage, Inventory

# Servicio para registrar un beneficiario con fecha
def register_beneficiary_with_region(data):
    new_beneficiary = {
        "name": data.get('name'),
        "satisfaction": data.get('satisfaction', 0),
        "date_registered": datetime.strptime(data.get('date'), '%Y-%m-%d').isoformat(),  # Convert to string
        "region": data.get('region')
    }
    result = supabase.table('beneficiaries').insert(new_beneficiary).execute()
    return result.data

# Servicio para obtener el número de beneficiarios por mes
def get_beneficiaries_per_month():
    count_per_month = defaultdict(int)
    result = supabase.table('beneficiaries').select('*').execute()

    for beneficiary in result.data:
        month = datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m')
        count_per_month[month] += 1

    return count_per_month

# Servicio para obtener el número de beneficiarios por día en el mes actual
def get_beneficiaries_per_day():
    current_month = datetime.now().strftime('%Y-%m')
    count_per_day = defaultdict(int)

    result = supabase.table('beneficiaries').select('*').ilike('date_registered', f'{current_month}%').execute()

    for beneficiary in result.data:
        day = datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
        count_per_day[day] += 1

    return count_per_day

# Servicio para registrar un ranking de paquete de comida
def register_food_package_ranking(data):
    new_package = {
        "info": data.get('info'),
        "date_rated": datetime.strptime(data.get('date'), '%Y-%m-%d').isoformat()  # Convert to string
    }
    
    # Check if package already exists
    package_result = supabase.table('food_packages').select('id').eq('id', data.get('id')).execute()
    
    if not package_result.data:
        # If package doesn't exist, insert it
        result = supabase.table('food_packages').insert(new_package).execute()
    
    # Insert satisfaction score in food_package_ratings table
    rating_data = {
        "food_package_id": data.get('id'),
        "satisfaction_score": data.get('satisfaction')
    }
    
    result = supabase.table('food_package_ratings').insert(rating_data).execute()
    return result.data

# Servicio para obtener el promedio de satisfacción por paquete mes a mes
def get_food_package_rankings_per_month():
    rankings_per_month = defaultdict(lambda: defaultdict(list))
    
    result = supabase.table('food_package_ratings').select('food_package_id, satisfaction_score, created_at').execute()
    
    for rating in result.data:
        month = datetime.strptime(rating['created_at'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m')
        package_info = supabase.table('food_packages').select('info').eq('id', rating['food_package_id']).execute()
        
        avg_satisfaction = rating['satisfaction_score']
        rankings_per_month[month][package_info.data[0]['info']].append(avg_satisfaction)
    
    # Calculate average satisfaction for each package per month
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

    result = supabase.table('beneficiaries').select('*').eq('region', region).execute()

    for beneficiary in result.data:
        if start_date <= datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S') <= end_date:
            month = datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m')
            trends[month] += 1

    return trends

# Servicio para predecir el número de beneficiarios en el futuro
def predict_future_beneficiaries(region, period):
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)

    trends = get_beneficiary_trends_by_region(region, one_year_ago, today)
    monthly_counts = list(trends.values())
    
    if len(monthly_counts) < 2:
        return {"error": "No hay suficientes datos históricos para predecir."}

    growth_rates = [
        (monthly_counts[i] - monthly_counts[i - 1]) / monthly_counts[i - 1]
        for i in range(1, len(monthly_counts))
        if monthly_counts[i - 1] > 0
    ]

    avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0

    last_month_count = monthly_counts[-1]
    predictions = {}

    for i in range(1, period + 1):
        next_month = (today + timedelta(days=30 * i)).strftime('%Y-%m')
        last_month_count += math.ceil(last_month_count * avg_growth_rate)
        predictions[next_month] = last_month_count

    return predictions

def update_inventory(data):
    # Prepare the inventory update, converting datetime to a string
    inventory_update = {
        "non_perishables": data.get('non_perishables', 0),
        "cereals": data.get('cereals', 0),
        "fruits_vegetables": data.get('fruits_vegetables', 0),
        "dairy": data.get('dairy', 0),
        "meat": data.get('meat', 0),
        "last_updated": datetime.now().isoformat()  # Convert datetime to ISO 8601 string
    }

    try:
        # Check if inventory exists (assuming id=1 for a single-row inventory)
        check_result = supabase.table('inventory').select('*').eq('id', 1).execute()

        if check_result.data:
            # If inventory exists, update it
            result = supabase.table('inventory').update(inventory_update).eq('id', 1).execute()
            return {"message": "Inventory updated", "inventory": result.data}
        else:
            # If no inventory exists, insert a new row
            result = supabase.table('inventory').insert(inventory_update).execute()
            return {"message": "Inventory created", "inventory": result.data}
    
    except Exception as e:
        # Catch any exceptions that occurred during the API request
        return {"message": "Failed to update inventory", "error": str(e)}
    

# Servicio para obtener el inventario total actual
def get_total_inventory():
    # Fetch the inventory data from the Supabase table
    result = supabase.table('inventory').select('*').eq('id', 1).execute()  # Assuming single-row inventory with id=1
    
    # Check if data exists
    if result.data and len(result.data) > 0:
        # Return the inventory as JSON
        inventory_data = result.data[0]  # Since the query returns a list of rows
        return {
            "non_perishables": inventory_data.get("non_perishables", 0),
            "cereals": inventory_data.get("cereals", 0),
            "fruits_vegetables": inventory_data.get("fruits_vegetables", 0),
            "dairy": inventory_data.get("dairy", 0),
            "meat": inventory_data.get("meat", 0),
            "last_updated": inventory_data.get("last_updated", None)
        }
    else:
        return {"error": "No inventory data found."}

# Servicio para registrar donaciones por semana y mes
def record_donations(data):
    new_donation = {
        "donation_date": datetime.now().isoformat(),  # Convert to string
        "non_perishables": data.get('non_perishables', 0),
        "cereals": data.get('cereals', 0),
        "fruits_vegetables": data.get('fruits_vegetables', 0),
        "dairy": data.get('dairy', 0),
        "meat": data.get('meat', 0)
    }
    
    result = supabase.table('donations').insert(new_donation).execute()
    return result.data

# Servicio para obtener las donaciones por mes
def get_donations_per_month():
    current_month = datetime.now().strftime('%Y-%m')
    result = supabase.table('donations').select('*').ilike('donation_date', f'{current_month}%').execute()
    return result.data

# Servicio para obtener las donaciones por semana
def get_donations_per_week():
    current_week = datetime.now().strftime('%Y-%U')
    result = supabase.table('donations').select('*').ilike('donation_date', f'{current_week}%').execute()
    return result.data