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


