# AidfoodMx - Backend

Este es el backend del proyecto **AidfoodMx**, que utiliza Flask para gestionar la lógica y las API que interactúan con los beneficiarios de BAMX. El proyecto permite registrar beneficiarios, analizar su satisfacción y gestionar las tandas de donaciones.

## Requerimientos

Para ejecutar este proyecto localmente, necesitarás tener instalados los siguientes programas:

- **Python 3.8+**
- **pip** (el gestor de paquetes de Python)
- Un entorno virtual de Python (recomendado)

## ejemplos de uso de los endpoints 
# AidFoodMX Backend API

This section describes the API endpoints for managing inventory and donations.

## 1. Update Inventory

- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/update_inventory`
- **Body Example (JSON):**
  ```json
  {
    "non_perishables": 10,
    "cereals": 5,
    "fruits_vegetables": 12,
    "dairy": 4,
    "meat": 3
  }
   ```

  	•	Description: Updates the current inventory by adding the specified quantities of each item category (non-perishables, cereals, fruits and vegetables, dairy, and meat).

2. Record Donations

	•	Method: POST
	•	URL: http://127.0.0.1:5000/record_donations
	•	Body Example (JSON):
  ```json
    {
  "non_perishables": 5,
  "cereals": 2,
  "fruits_vegetables": 7,
  "dairy": 1,
  "meat": 2
  } 
  ```  
 


	•	Description: Records donations received and updates the donation count for the current month and week based on the date of the request.

3. Get Total Inventory

	•	Method: GET
	•	URL: http://127.0.0.1:5000/get_total_inventory
	•	Response Example (JSON):
  ```json
{
  "total_inventory": {
    "non_perishables": 100,
    "cereals": 50,
    "fruits_vegetables": 70,
    "dairy": 30,
    "meat": 25,
    "last_updated": "2024-09-24T10:00:00"
  }
}
  ``` 

  	•	Description: Retrieves the current total inventory of each item category (non-perishables, cereals, fruits and vegetables, dairy, and meat).

4. Get Donations Per Month

	•	Method: GET
	•	URL: http://127.0.0.1:5000/get_donations_per_month
	•	Response Example (JSON):
  ```json
    {
  "donations_per_month": {
    "2024-09": {
      "non_perishables": 100,
      "cereals": 50,
      "fruits_vegetables": 70,
      "dairy": 30,
      "meat": 25
    },
    "2024-10": {
      "non_perishables": 80,
      "cereals": 40,
      "fruits_vegetables": 60,
      "dairy": 25,
      "meat": 20
    }
  }
}

  ``` 

  	•	Description: Returns the total donations received for each category by month.

5. Get Donations Per Week

	•	Method: GET
	•	URL: http://127.0.0.1:5000/get_donations_per_week
	•	Response Example (JSON):
  ```json
    {
  "donations_per_week": {
    "2024-38": {
      "non_perishables": 50,
      "cereals": 25,
      "fruits_vegetables": 35,
      "dairy": 15,
      "meat": 10
    },
    "2024-39": {
      "non_perishables": 30,
      "cereals": 15,
      "fruits_vegetables": 20,
      "dairy": 10,
      "meat": 5
    }
  }
}

  ``` 

http://127.0.0.1:5000/get_donations_per_month 

http://127.0.0.1:5000/get_donations_per_week


http://127.0.0.1:5000/record_donations

input expected: 
    {
        "donation_date": "2024-01-10T14:30:00",  
        "non_perishables": 10,
        "cereals": 5,
        "fruits_vegetables": 8,
        "dairy": 2,
        "meat": 4
    }


    record multiple donations 

    http://127.0.0.1:5000/record_multiple_donations

    [
    {
        "donation_date": "2024-01-10T14:30:00",  
        "non_perishables": 10,
        "cereals": 5,
        "fruits_vegetables": 8,
        "dairy": 2,
        "meat": 4
    },
    {
        "donation_date": "2024-02-15T10:00:00", 
        "non_perishables": 15,
        "cereals": 8,
        "fruits_vegetables": 7,
        "dairy": 3,
        "meat": 6
    },
    {
        "donation_date": "2024-03-01T12:45:00",  
        "non_perishables": 12,
        "cereals": 10,
        "fruits_vegetables": 15,
        "dairy": 4,
        "meat": 5
    }
]



  	•	Description: Returns the total donations received for each category by week (week number based on the year).


http://127.0.0.1:5000/register_food_package_ranking

{
    "info": "Package A",
    "date": "2024-09-25",
    "satisfaction": 5
}

and like this we get 
http://127.0.0.1:5000/get_food_package_rankings_per_month


Also we have the endpoint to register beneficiaries and multiple beneficiaries 
here is an example to use the one to register beneficiaries individually 
http://127.0.0.1:5000/register_beneficiary_with_region

example of body: 
{
        "name": "María López",
        "satisfaction": 4,
        "date": "2024-02-15",
        "region": "Querétaro"
    }

    and this is the one to register multiple beneficiaries: 

    http://127.0.0.1:5000/register_multiple_beneficiaries

    and here is an exampel of an input: [
    {
        "name": "Carlos Perez",
        "satisfaction": 5,
        "date": "2024-10-01",
        "region": "Ciudad de México"
    },
    {
        "name": "German nalgotas",
        "satisfaction": 4,
        "date": "2024-01-25",
        "region": "Guadalajara"
    },
    {
        "name": "Luis Martinez",
        "satisfaction": 3,
        "date": "2024-10-10",
        "region": "Monterrey"
    },
    {
        "name": "María López",
        "satisfaction": 4,
        "date": "2024-02-15",
        "region": "Querétaro"
    },
    {
        "name": "Juan Hernandez",
        "satisfaction": 5,
        "date": "2024-10-30",
        "region": "Puebla"
    },
    {
        "name": "Sofia Gutierrez",
        "satisfaction": 2,
        "date": "2024-03-05",
        "region": "León"
    },
    {
        "name": "Miguel Ramirez",
        "satisfaction": 4,
        "date": "2024-02-20",
        "region": "Tijuana"
    },
    {
        "name": "Elena Sanchez",
        "satisfaction": 3,
        "date": "2024-02-28",
        "region": "Toluca"
    },
    {
        "name": "Diego Vargas",
        "satisfaction": 5,
        "date": "2024-01-18",
        "region": "Aguascalientes"
    },
    {
        "name": "Fernanda Morales",
        "satisfaction": 5,
        "date": "2024-03-12",
        "region": "Mérida"
    }
] 



now to get the info of these beneficiaries

this endpoint return us the number of beneficiaties which have been registered each 
day of the month: 
http://127.0.0.1:5000/get_beneficiaries_per_day

this one gives us the number of beneficiaries that have been registered each month of hte year: 

http://127.0.0.1:5000/get_beneficiaries_per_month


we also have the one to register package rankings of food  

this one: http://127.0.0.1:5000/register_food_package_ranking
and here is an example of the body: 

{
        "info": "Package S",
        "date": "2024-09-19",
        "satisfaction": 5
    }

    we can also register multiple packages with this endpoint: 
    http://127.0.0.1:5000/register_multiple_food_package_rankings

    we can use it like this: 
    [
    {
        "info": "Package A",
        "date": "2024-09-01",
        "satisfaction": 5
    },
    {
        "info": "Package B",
        "date": "2024-09-02",
        "satisfaction": 4
    },
    {
        "info": "Package C",
        "date": "2024-09-03",
        "satisfaction": 3
    },
    {
        "info": "Package D",
        "date": "2024-09-04",
        "satisfaction": 5
    },
    {
        "info": "Package E",
        "date": "2024-09-05",
        "satisfaction": 2
    },
    {
        "info": "Package F",
        "date": "2024-09-06",
        "satisfaction": 4
    }
]


And using this endpoint, we can see how a package was rated by the community each month.
http://127.0.0.1:5000/get_food_package_rankings_per_month
example of output: 
{
    "data": {
        "2024-10": {
            "Package A": 5.0,
            "Package A33": 2.0,
            "Package B": 4.0,
            "Package C": 3.0,
            "Package D": 5.0,
            "Package E": 2.0,
            "Package F": 4.0,
            "Package G": 3.0,
            "Package H": 5.0,
            "Package I": 2.0,
            "Package J": 4.0,
            "Package K": 3.0,
            "Package L": 5.0,
            "Package M": 1.0,
            "Package N": 4.0,
            "Package O": 2.0,
            "Package P": 5.0,
            "Package Q": 3.0,
            "Package R": 4.0,
            "Package S": 5.0,
            "Package T": 2.0
        }
    }
}


This endpoint predicts future beneficiaries for a given region over a specified period. It analyzes historical data from the last year to calculate monthly growth rates, then applies these rates to forecast future beneficiaries. The prediction technique uses time-series analysis by calculating the average monthly growth rate and projecting future trends based on these growth patterns.


http://127.0.0.1:5000/predict_future_beneficiaries?region=Guadalajara&period=6

example output: 

{
    "message": "Future beneficiary predictions generated",
    "predictions": {
        "2024-11": 5,
        "2024-12": 12,
        "2025-01": 18,
        "2025-03": 41
    },
    "region": "Guadalajara"
}


The /get_beneficiary_trends_by_region endpoint retrieves the trends of beneficiaries registered in a specific region over a given time range. It accepts query parameters for the region, start date, and end date, then returns the count of beneficiaries grouped by month within that period.

How It Works:

	•	Input: You provide a region (e.g., “Guadalajara”) and a time range (start and end dates).
	•	Processing: The system queries the beneficiaries table, filters by region and the provided date range, and groups the results by month.
	•	Output: A JSON response that contains the count of beneficiaries for each month within the selected period.

Use Cases:

	1.	Regional Analysis: Evaluate the beneficiary trends in different regions to understand where more help is being provided.
	2.	Time-based Insights: Analyze how the number of beneficiaries changes over time, such as before and after major events or campaigns.
	3.	Forecasting: Combined with future prediction models, the data can help predict the future needs for beneficiaries in specific regions.

http://127.0.0.1:5000/get_beneficiary_trends_by_region?region=Guadalajara&start_date=2024-01-01&end_date=2024-12-31 

example output: 

{
    "message": "Beneficiary trends retrieved",
    "trends": {
        "2024-01": 2,
        "2024-09": 3
    }
}