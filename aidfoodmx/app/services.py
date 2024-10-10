from datetime import datetime, timedelta
from collections import defaultdict
import math
import requests
from supabase_client import supabase
from .models import Beneficiary, FoodPackage, Inventory
from config import GEMINI_API_KEY  # Make sure your GEMINI_API_KEY is in the .env file
import json


# Initialize the Gemini API Client for generating insights
class GeminiAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
        self.headers = {'Content-Type': 'application/json'}

    def generate_content_stream(self, prompt_text):
        url = f"{self.api_url}?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt_text}]}]
        }
        try:
            with requests.post(url, headers=self.headers, data=json.dumps(payload), stream=True) as response:
                if response.status_code == 200:
                    content = ""
                    for chunk in response.iter_content(chunk_size=None):
                        if chunk:
                            content += chunk.decode('utf-8')
                    return content
                else:
                    return {"error": response.status_code, "message": response.text}
        except Exception as e:
            return {"error": str(e)}

# Initialize the Gemini client
gemini_client = GeminiAPIClient(api_key=GEMINI_API_KEY)

def generate_single_insight(prompt_text):
    """Helper function to generate a single insight using the Gemini API."""
    try:
        insights_raw = gemini_client.generate_content_stream(prompt_text)
        response_json = json.loads(insights_raw)
        # Extract the content from the first candidate
        insights_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
        return insights_text
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing Gemini response: {str(e)}")
        return "No se pudo generar el insight."

def generate_insights(region):
    # Get beneficiary trends for the region
    trends = get_beneficiary_trends_by_region(region, datetime.now() - timedelta(days=365), datetime.now())

    # Get donation patterns per month
    donation_patterns = get_kind_of_donations_per_month()

    # Get current inventory data
    inventory_data = get_total_inventory()

    # Get food package satisfaction rankings per month
    satisfaction_rankings = get_food_package_rankings_per_month()

    # Build separate prompts for each insight
    prompt_beneficiary_trend = f"Genera un breve resumen sobre las tendencias de beneficiarios en la región {region} con base en los siguientes datos: {trends['trends']}. Proporciónalo en un solo punto clave."
    
    prompt_donation_patterns = f"Genera un breve resumen sobre los patrones de donaciones por mes en la región {region} con base en los siguientes datos: {donation_patterns['donations_per_month']}. Proporciónalo en un solo punto clave."
    
    prompt_inventory = f"Genera un breve resumen sobre el estado del inventario en la región {region} con base en los siguientes datos: {inventory_data}. Proporciónalo en un solo punto clave."
    
    prompt_satisfaction = f"Genera un breve resumen sobre la satisfacción de los paquetes de alimentos en la región {region} con base en los siguientes datos: {satisfaction_rankings}. Proporciónalo en un solo punto clave."

    # Get insights for each category
    insight_beneficiary_trend = generate_single_insight(prompt_beneficiary_trend)
    insight_donation_patterns = generate_single_insight(prompt_donation_patterns)
    insight_inventory = generate_single_insight(prompt_inventory)
    insight_satisfaction = generate_single_insight(prompt_satisfaction)

    # Return insights in a clean JSON format
    insights_json = {
        "insights": [
            {"punto": insight_beneficiary_trend},
            {"punto": insight_donation_patterns},
            {"punto": insight_inventory},
            {"punto": insight_satisfaction}
        ]
    }

    return insights_json
# Service to register a beneficiary with region
def register_beneficiary_with_region(data):
    new_beneficiary = {
        "name": data.get('name'),
        "satisfaction": data.get('satisfaction', 0),
        "date_registered": datetime.strptime(data.get('date'), '%Y-%m-%d').isoformat(),
        "region": data.get('region')
    }
    try:
        result = supabase.table('beneficiaries').insert(new_beneficiary).execute()
        return {"message": "Beneficiary registered", "beneficiary": result.data}
    except Exception as e:
        return {"message": "Failed to register beneficiary", "error": str(e)}

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
    
    # Servicio para registrar múltiples beneficiarios con región
def register_multiple_beneficiaries(beneficiaries):
    try:
        beneficiaries_to_insert = []
        
        for data in beneficiaries:
            new_beneficiary = {
                "name": data.get('name'),
                "satisfaction": data.get('satisfaction', 0),
                "date_registered": datetime.strptime(data.get('date'), '%Y-%m-%d').isoformat(),  # Convert to string
                "region": data.get('region')
            }
            beneficiaries_to_insert.append(new_beneficiary)

        # Insert all beneficiaries at once
        result = supabase.table('beneficiaries').insert(beneficiaries_to_insert).execute()
        
        return {"message": "Multiple beneficiaries registered", "beneficiaries": result.data}
    except Exception as e:
        return {"message": "Failed to register multiple beneficiaries", "error": str(e)}

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
    current_month_start = datetime.now().replace(day=1)  # Get the first day of the current month
    next_month_start = (current_month_start + timedelta(days=32)).replace(day=1)  # Get the first day of the next month
    count_per_day = defaultdict(int)

    try:
        # Fetch all beneficiaries registered between the first day of the current month and the first day of the next month
        result = supabase.table('beneficiaries').select('*').gte('date_registered', current_month_start.isoformat()).lt('date_registered', next_month_start.isoformat()).execute()

        # Process each beneficiary
        for beneficiary in result.data:
            day = datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
            count_per_day[day] += 1

        return count_per_day
    except Exception as e:
        return {"message": "Failed to get beneficiaries per day", "error": str(e)}
# Servicio para registrar un ranking de paquete de comida

def register_food_package_ranking(data):
    try:
        # Step 1: Check if the package already exists by searching for the info
        package_result = supabase.table('food_packages').select('id').eq('info', data.get('info')).execute()

        # Step 2: If package doesn't exist, insert it
        if package_result.data == []:
            new_package = {
                "info": data.get('info'),
                "date_rated": datetime.strptime(data.get('date'), '%Y-%m-%d').isoformat()  # Convert to string
            }
            insert_result = supabase.table('food_packages').insert(new_package).execute()

            # Check for errors in the insert operation
            if 'error' in insert_result:
                return {"message": "Failed to insert food package", "error": insert_result['error']}

            # Get the newly inserted package ID
            food_package_id = insert_result.data[0]['id']
        else:
            # If the package exists, retrieve its ID
            food_package_id = package_result.data[0]['id']

        # Step 3: Insert the satisfaction score into the 'food_package_ratings' table
        rating_data = {
            "food_package_id": food_package_id,
            "satisfaction_score": data.get('satisfaction')
        }

        rating_result = supabase.table('food_package_ratings').insert(rating_data).execute()

        # Check for errors in the rating insert
        if 'error' in rating_result:
            return {"message": "Failed to insert food package rating", "error": rating_result['error']}

        return {"message": "Rating registered successfully", "rating": rating_result.data}

    except Exception as e:
        return {"message": "Failed to register food package rating", "error": str(e)}


def register_multiple_food_package_rankings(rankings):
    try:
        rankings_to_insert = []

        for ranking in rankings:
            # Check if package already exists by searching for the info
            package_result = supabase.table('food_packages').select('id').eq('info', ranking.get('info')).execute()

            if package_result.data == []:
                # If package doesn't exist, insert it
                new_package = {
                    "info": ranking.get('info'),
                    "date_rated": datetime.strptime(ranking.get('date'), '%Y-%m-%d').isoformat()  # Convert to string
                }
                insert_result = supabase.table('food_packages').insert(new_package).execute()

                # Check for errors during insertion
                if 'error' in insert_result:
                    return {"message": "Failed to insert food package", "error": insert_result['error']}

                # Get the newly inserted package ID
                food_package_id = insert_result.data[0]['id']
            else:
                # If package exists, get its ID
                food_package_id = package_result.data[0]['id']

            # Prepare satisfaction score data
            rating_data = {
                "food_package_id": food_package_id,
                "satisfaction_score": ranking.get('satisfaction')
            }
            rankings_to_insert.append(rating_data)

        # Insert all rankings at once
        result = supabase.table('food_package_ratings').insert(rankings_to_insert).execute()

        # Check for errors during insertion
        if 'error' in result:
            return {"message": "Failed to insert food package rankings", "error": result['error']}

        return {"message": "Multiple food package rankings registered successfully", "rankings": result.data}

    except Exception as e:
        return {"message": "Failed to register multiple food package rankings", "error": str(e)}
    try:
        rankings_to_insert = []
        
        for ranking in rankings:
            # Check if package already exists by searching for the info
            package_result = supabase.table('food_packages').select('id').eq('info', ranking.get('info')).execute()

            if not package_result.data:
                # If package doesn't exist, insert it
                new_package = {
                    "info": ranking.get('info'),
                    "date_rated": datetime.strptime(ranking.get('date'), '%Y-%m-%d').isoformat()  # Convert to string
                }
                insert_result = supabase.table('food_packages').insert(new_package).execute()
                food_package_id = insert_result.data[0]['id']
            else:
                # If package exists, get its ID
                food_package_id = package_result.data[0]['id']

            # Prepare satisfaction score data
            rating_data = {
                "food_package_id": food_package_id,
                "satisfaction_score": ranking.get('satisfaction')
            }
            rankings_to_insert.append(rating_data)

        # Insert all rankings at once
        result = supabase.table('food_package_ratings').insert(rankings_to_insert).execute()

        return {"message": "Multiple food package rankings registered", "rankings": result.data}
    except Exception as e:
        return {"message": "Failed to register multiple food package rankings", "error": str(e)}
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
        # Ensure start_date and end_date are properly formatted as strings (ISO 8601)
        start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%S')
        end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%S')

        # Filter beneficiaries by region and date range using ISO 8601 string format
        result = supabase.table('beneficiaries').select('*').eq('region', region).gte('date_registered', start_date_str).lte('date_registered', end_date_str).execute()

        # Process the result to aggregate beneficiaries by month
        for beneficiary in result.data:
            # Parse date and group by month (YYYY-MM format)
            month = datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m')
            trends[month] += 1

        return {"message": "Beneficiary trends retrieved", "trends": trends}
    except Exception as e:
        return {"message": "Failed to get beneficiary trends", "error": str(e)}
    
    
def predict_future_beneficiaries(region, period):
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)

    try:
        # Query to get beneficiaries data by region from the last year
        result = supabase.table('beneficiaries').select('date_registered').eq('region', region).gte('date_registered', one_year_ago.isoformat()).execute()

        # Check if we have any data for that region
        if not result.data:
            return {"error": f"No historical data available for region '{region}'"}

        monthly_counts = defaultdict(int)

        # Calculate the number of beneficiaries registered per month
        for beneficiary in result.data:
            month = datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m')
            monthly_counts[month] += 1

        if len(monthly_counts) < 2:
            return {"error": "Not enough historical data to predict future beneficiaries."}

        # Calculate monthly growth rates
        sorted_months = sorted(monthly_counts.keys())
        growth_rates = []
        for i in range(1, len(sorted_months)):
            prev_month = sorted_months[i - 1]
            curr_month = sorted_months[i]
            if monthly_counts[prev_month] > 0:
                growth_rate = (monthly_counts[curr_month] - monthly_counts[prev_month]) / monthly_counts[prev_month]
                growth_rates.append(growth_rate)

        avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0

        # Predict future beneficiaries for the next 'period' months
        last_month_count = monthly_counts[sorted_months[-1]]
        predictions = {}

        for i in range(1, period + 1):
            next_month = (today + timedelta(days=30 * i)).strftime('%Y-%m')
            last_month_count += math.ceil(last_month_count * avg_growth_rate)
            predictions[next_month] = last_month_count

        return {"message": "Future beneficiary predictions generated", "predictions": predictions, "region": region}
    except Exception as e:
        return {"message": "Failed to predict future beneficiaries", "error": str(e)}
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)

    try:
        # Query to get beneficiaries data by region from the last year
        result = supabase.table('beneficiaries').select('date_registered').eq('region', region).gte('date_registered', one_year_ago.isoformat()).execute()

        if not result.data:
            return {"error": f"No historical data available for region '{region}'"}

        monthly_counts = defaultdict(int)

        # Calculate the number of beneficiaries registered per month
        for beneficiary in result.data:
            month = datetime.strptime(beneficiary['date_registered'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m')
            monthly_counts[month] += 1

        if len(monthly_counts) < 2:
            return {"error": "Not enough historical data to predict future beneficiaries."}

        # Calculate monthly growth rates
        sorted_months = sorted(monthly_counts.keys())
        growth_rates = []
        for i in range(1, len(sorted_months)):
            prev_month = sorted_months[i - 1]
            curr_month = sorted_months[i]
            if monthly_counts[prev_month] > 0:
                growth_rate = (monthly_counts[curr_month] - monthly_counts[prev_month]) / monthly_counts[prev_month]
                growth_rates.append(growth_rate)

        avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0

        # Predict future beneficiaries for the next 'period' months
        last_month_count = monthly_counts[sorted_months[-1]]
        predictions = {}

        for i in range(1, period + 1):
            next_month = (today + timedelta(days=30 * i)).strftime('%Y-%m')
            last_month_count += math.ceil(last_month_count * avg_growth_rate)
            predictions[next_month] = last_month_count

        return {"message": "Future beneficiary predictions generated", "predictions": predictions, "region": region}
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
        "donation_date": datetime.now().isoformat(),
        "non_perishables": data.get('non_perishables', 0),
        "cereals": data.get('cereals', 0),
        "fruits_vegetables": data.get('fruits_vegetables', 0),
        "dairy": data.get('dairy', 0),
        "meat": data.get('meat', 0),
        "donator": data.get('donator'),  # New field for donator
        "region": data.get('region')  # New field for region
    }

    try:
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
            start_of_month = datetime(current_year, month, 1)
            if month == 12:
                next_month = datetime(current_year + 1, 1, 1)
            else:
                next_month = datetime(current_year, month + 1, 1)

            # Hacer la consulta para obtener las donaciones entre el primer día y el siguiente mes
            result = supabase.table('donations').select('*').gte('donation_date', start_of_month.isoformat()).lt('donation_date', next_month.isoformat()).execute()
            
            # Almacenar el número de donaciones para el mes actual
            donations_per_month[start_of_month.strftime('%Y-%m')] = len(result.data)
        
        return donations_per_month
    except Exception as e:
        return {"message": "Failed to get donations per month of year", "error": str(e)}
    
def get_top_donators_per_region(region):
    try:
        # Query donations by region and group by donator
        result = supabase.table('donations').select('donator, COUNT(*) as total_donations').eq('region', region).group('donator').execute()

        # Sort the result by total donations and return the top donators
        top_donators = sorted(result.data, key=lambda x: x['total_donations'], reverse=True)

        return {"message": "Top donators per region", "top_donators": top_donators}
    except Exception as e:
        return {"message": "Failed to get top donators per region", "error": str(e)}
    
    
# Servicio para obtener las donaciones por semana

def get_kind_of_donations_per_month():
    try:
        current_year = datetime.now().year
        
        donations_per_month = defaultdict(lambda: {
            "non_perishables": 0,
            "cereals": 0,
            "fruits_vegetables": 0,
            "dairy": 0,
            "meat": 0,
            "donators": set(),  # To hold unique donators
            "regions": set()  # To hold regions
        })
        
        for month in range(1, 13):
            start_of_month = datetime(current_year, month, 1)
            next_month = datetime(current_year + 1, 1, 1) if month == 12 else datetime(current_year, month + 1, 1)

            result = supabase.table('donations').select('*').gte('donation_date', start_of_month.isoformat()).lt('donation_date', next_month.isoformat()).execute()

            for donation in result.data:
                donations_per_month[start_of_month.strftime('%Y-%m')]["non_perishables"] += donation.get('non_perishables', 0)
                donations_per_month[start_of_month.strftime('%Y-%m')]["cereals"] += donation.get('cereals', 0)
                donations_per_month[start_of_month.strftime('%Y-%m')]["fruits_vegetables"] += donation.get('fruits_vegetables', 0)
                donations_per_month[start_of_month.strftime('%Y-%m')]["dairy"] += donation.get('dairy', 0)
                donations_per_month[start_of_month.strftime('%Y-%m')]["meat"] += donation.get('meat', 0)
                donations_per_month[start_of_month.strftime('%Y-%m')]["donators"].add(donation.get('donator'))
                donations_per_month[start_of_month.strftime('%Y-%m')]["regions"].add(donation.get('region'))
        
        # Convert sets to lists for JSON serialization
        for month in donations_per_month:
            donations_per_month[month]["donators"] = list(donations_per_month[month]["donators"])
            donations_per_month[month]["regions"] = list(donations_per_month[month]["regions"])
        
        return {"donations_per_month": donations_per_month}
    except Exception as e:
        return {"message": "Failed to get kind of donations per month", "error": str(e)}
    try:
        # Get the current year
        current_year = datetime.now().year
        
        # Dictionary to store donation types per month
        donations_per_month = defaultdict(lambda: {
            "non_perishables": 0,
            "cereals": 0,
            "fruits_vegetables": 0,
            "dairy": 0,
            "meat": 0
        })
        
        # Iterate over the 12 months of the year
        for month in range(1, 13):
            # Get the first day of the current month
            start_of_month = datetime(current_year, month, 1)
            
            # Get the first day of the next month
            if month == 12:
                next_month = datetime(current_year + 1, 1, 1)
            else:
                next_month = datetime(current_year, month + 1, 1)

            # Fetch donations between the first day of the current month and the next month
            result = supabase.table('donations').select('*').gte('donation_date', start_of_month.isoformat()).lt('donation_date', next_month.isoformat()).execute()
            
            # Process each donation and accumulate the totals for each type
            for donation in result.data:
                donations_per_month[start_of_month.strftime('%Y-%m')]["non_perishables"] += donation.get('non_perishables', 0)
                donations_per_month[start_of_month.strftime('%Y-%m')]["cereals"] += donation.get('cereals', 0)
                donations_per_month[start_of_month.strftime('%Y-%m')]["fruits_vegetables"] += donation.get('fruits_vegetables', 0)
                donations_per_month[start_of_month.strftime('%Y-%m')]["dairy"] += donation.get('dairy', 0)
                donations_per_month[start_of_month.strftime('%Y-%m')]["meat"] += donation.get('meat', 0)
        
        return {"donations_per_month": donations_per_month}
    except Exception as e:
        return {"message": "Failed to get kind of donations per month", "error": str(e)}
    
def get_donations_per_week():
    try:
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        result = supabase.table('donations').select('*').gte('donation_date', start_of_week.isoformat()).lte('donation_date', end_of_week.isoformat()).execute()

        donations = []
        for donation in result.data:
            donations.append({
                "donation_date": donation.get('donation_date'),
                "non_perishables": donation.get('non_perishables', 0),
                "cereals": donation.get('cereals', 0),
                "fruits_vegetables": donation.get('fruits_vegetables', 0),
                "dairy": donation.get('dairy', 0),
                "meat": donation.get('meat', 0),
                "donator": donation.get('donator'),
                "region": donation.get('region')
            })

        return {"donations_per_week": donations}
    except Exception as e:
        return {"message": "Failed to get donations per week", "error": str(e)}
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
                "meat": donation.get('meat', 0),
                "donator": donation.get('donator'),  # New field for donator
                "region": donation.get('region')  # New field for region
            }
            donations_to_insert.append(new_donation)

        # Insertar todas las donaciones en un solo comando
        result = supabase.table('donations').insert(donations_to_insert).execute()

        return {"message": "Multiple donations recorded", "donations": result.data}
    except Exception as e:
        return {"message": "Failed to record multiple donations", "error": str(e)}
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
    
def get_top_donators_per_region(region):
    try:
        result = supabase.table('donations').select('donator, COUNT(*) as total').eq('region', region).group('donator').order('total', desc=True).execute()

        return {"top_donators": result.data}
    except Exception as e:
        return {"message": "Failed to get top donators per region", "error": str(e)}
    
def get_top_donators_global():
    try:
        result = supabase.table('donations').select('donator, COUNT(*) as total').group('donator').order('total', desc=True).execute()

        return {"top_donators_global": result.data}
    except Exception as e:
        return {"message": "Failed to get top donators globally", "error": str(e)}
# Service to get all distinct regions from the beneficiaries table
def get_all_regions():
    try:
        # Query to get all regions from the beneficiaries table
        result = supabase.table('beneficiaries').select('region').execute()

        # Extract regions from the result and remove duplicates
        regions = list(set(beneficiary['region'] for beneficiary in result.data if 'region' in beneficiary))

        return {"message": "Regions retrieved", "regions": regions}
    except Exception as e:
        return {"message": "Failed to retrieve regions", "error": str(e)}