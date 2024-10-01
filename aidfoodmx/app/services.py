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
    
    try:
        result = supabase.table('beneficiaries').insert(new_beneficiary).execute()
        return {"message": "Beneficiary registered", "beneficiary": result.data}
    except Exception as e:
        return {"message": "Failed to register beneficiary", "error": str(e)}

# Servicio para obtener el número de beneficiarios por mes
def get_beneficiaries_per_month():
    count_per_month = defaultdict(int)

    try:
        result = supabase.table('beneficiaries').select('*').execute()

        for beneficiary in result.data:
            month = datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m')
            count_per_month[month] += 1

        return count_per_month
    except Exception as e:
        return {"message": "Failed to get beneficiaries per month", "error": str(e)}

# Servicio para obtener el número de beneficiarios por día en el mes actual
def get_beneficiaries_per_day():
    current_month = datetime.now().strftime('%Y-%m')
    count_per_day = defaultdict(int)

    try:
        result = supabase.table('beneficiaries').select('*').ilike('date_registered', f'{current_month}%').execute()

        for beneficiary in result.data:
            day = datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
            count_per_day[day] += 1

        return count_per_day
    except Exception as e:
        return {"message": "Failed to get beneficiaries per day", "error": str(e)}

# Servicio para registrar un ranking de paquete de comida
def register_food_package_ranking(data):
    try:
        # Check if package already exists by searching for the info
        package_result = supabase.table('food_packages').select('id').eq('info', data.get('info')).execute()

        if not package_result.data:
            # If package doesn't exist, insert it
            new_package = {
                "info": data.get('info'),
                "date_rated": datetime.strptime(data.get('date'), '%Y-%m-%d').isoformat()  # Convert to string
            }
            insert_result = supabase.table('food_packages').insert(new_package).execute()
            food_package_id = insert_result.data[0]['id']
        else:
            # If package exists, get its ID
            food_package_id = package_result.data[0]['id']

        # Insert satisfaction score in food_package_ratings table
        rating_data = {
            "food_package_id": food_package_id,
            "satisfaction_score": data.get('satisfaction')
        }

        result = supabase.table('food_package_ratings').insert(rating_data).execute()
        return {"message": "Rating registered", "rating": result.data}
    except Exception as e:
        return {"message": "Failed to register food package rating", "error": str(e)}
# Servicio para obtener el promedio de satisfacción por paquete mes a mes
# Servicio para obtener el promedio de satisfacción por paquete mes a mes
# Servicio para obtener el promedio de satisfacción por paquete mes a mes
def get_food_package_rankings_per_month():
    rankings_per_month = defaultdict(lambda: defaultdict(list))

    try:
        # Fetch all the ratings
        result = supabase.table('food_package_ratings').select('food_package_id, satisfaction_score, created_at').execute()

        # Process each rating
        for rating in result.data:
            # Extract the month from the 'created_at' timestamp, accounting for fractional seconds
            created_at = rating['created_at']
            try:
                # Try parsing with fractional seconds (microseconds)
                timestamp = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                # Fallback to parsing without fractional seconds
                timestamp = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S')

            # Extract the month
            month = timestamp.strftime('%Y-%m')
            
            # Fetch the package info based on 'food_package_id'
            package_info_result = supabase.table('food_packages').select('info').eq('id', rating['food_package_id']).execute()
            package_info = package_info_result.data[0]['info'] if package_info_result.data else "Unknown Package"
            
            # Add the satisfaction score to the respective month and package
            rankings_per_month[month][package_info].append(rating['satisfaction_score'])

        # Calculate the average satisfaction for each package per month
        averages_per_month = {
            month: {
                package_info: sum(scores) / len(scores)
                for package_info, scores in packages.items()
            }
            for month, packages in rankings_per_month.items()
        }

        return averages_per_month
    except Exception as e:
        return {"message": "Failed to get food package rankings", "error": str(e)}
# Servicio para obtener las tendencias de beneficiarios por región
def get_beneficiary_trends_by_region(region, start_date, end_date):
    trends = defaultdict(int)

    try:
        result = supabase.table('beneficiaries').select('*').eq('region', region).execute()

        for beneficiary in result.data:
            if start_date <= datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S') <= end_date:
                month = datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m')
                trends[month] += 1

        return trends
    except Exception as e:
        return {"message": "Failed to get beneficiary trends", "error": str(e)}

# Servicio para predecir el número de beneficiarios en el futuro
def predict_future_beneficiaries(region, period):
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)

    try:
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
    except Exception as e:
        return {"message": "Failed to predict future beneficiaries", "error": str(e)}
    
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
    try:
        result = supabase.table('inventory').select('*').eq('id', 1).execute()  # Assuming single-row inventory with id=1

        if result.data and len(result.data) > 0:
            # Return the inventory as JSON
            inventory_data = result.data[0]
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
    except Exception as e:
        return {"message": "Failed to get total inventory", "error": str(e)}

# Servicio para registrar donaciones por semana y mes
def record_donations(data):
    new_donation = {
        "donation_date": datetime.now().isoformat(),  # Inserta la fecha actual
        "non_perishables": data.get('non_perishables', 0),
        "cereals": data.get('cereals', 0),
        "fruits_vegetables": data.get('fruits_vegetables', 0),
        "dairy": data.get('dairy', 0),
        "meat": data.get('meat', 0)
    }

    try:
        # Inserta los datos en la tabla 'donations'
        result = supabase.table('donations').insert(new_donation).execute()
        return {"message": "Donation recorded", "donation": result.data}
    except Exception as e:
        return {"message": "Failed to record donation", "error": str(e)}
    
# Servicio para obtener las donaciones por mes
# Servicio para obtener el número de donaciones por mes del año actual
def get_donations_per_month_of_year():
    try:
        # Obtener el año actual
        current_year = datetime.now().year
        
        # Diccionario para almacenar el número de donaciones por mes
        donations_per_month = defaultdict(int)
        
        # Iterar sobre los 12 meses del año
        for month in range(1, 13):
            # Obtener el primer día del mes actual
            start_of_month = datetime(current_year, month, 1)
            # Obtener el primer día del siguiente mes
            if month == 12:
                # Si estamos en diciembre, el siguiente mes es enero del próximo año
                next_month = datetime(current_year + 1, 1, 1)
            else:
                # Si no estamos en diciembre, simplemente obtenemos el primer día del siguiente mes
                next_month = datetime(current_year, month + 1, 1)

            # Hacer la consulta para obtener las donaciones entre el primer día y el siguiente mes
            result = supabase.table('donations').select('*').gte('donation_date', start_of_month.isoformat()).lt('donation_date', next_month.isoformat()).execute()
            
            # Almacenar el número de donaciones para el mes actual
            donations_per_month[start_of_month.strftime('%Y-%m')] = len(result.data)
        
        return donations_per_month
    except Exception as e:
        return {"message": "Failed to get donations per month of year", "error": str(e)}
# Servicio para obtener las donaciones por semana
def get_donations_per_week():
    try:
        # Obtener el inicio de la semana actual (lunes)
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())  # Lunes de esta semana
        # Obtener el fin de la semana actual (domingo)
        end_of_week = start_of_week + timedelta(days=6)

        # Hacer la consulta para obtener las donaciones entre el lunes y domingo de la semana actual
        result = supabase.table('donations').select('*').gte('donation_date', start_of_week.isoformat()).lte('donation_date', end_of_week.isoformat()).execute()

        return result.data
    except Exception as e:
        return {"message": "Failed to get donations per week", "error": str(e)}
    
# Servicio para registrar múltiples donaciones, cada una con su propia fecha
def record_multiple_donations(donations):
    try:
        # Crear una lista de donaciones a partir de los datos proporcionados
        donations_to_insert = []
        for donation in donations:
            new_donation = {
                "donation_date": donation.get('donation_date', datetime.now().isoformat()),  # Si no se proporciona, se usa la fecha actual
                "non_perishables": donation.get('non_perishables', 0),
                "cereals": donation.get('cereals', 0),
                "fruits_vegetables": donation.get('fruits_vegetables', 0),
                "dairy": donation.get('dairy', 0),
                "meat": donation.get('meat', 0)
            }
            donations_to_insert.append(new_donation)

        # Insertar todas las donaciones en un solo comando
        result = supabase.table('donations').insert(donations_to_insert).execute()

        return {"message": "Multiple donations recorded", "donations": result.data}
    except Exception as e:
        return {"message": "Failed to record multiple donations", "error": str(e)}