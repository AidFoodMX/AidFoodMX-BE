
---

# AidfoodMx - Backend

Este es el backend del proyecto **AidfoodMx**, que utiliza Flask para gestionar la lógica y las API que interactúan con los beneficiarios de BAMX. El proyecto permite registrar beneficiarios, analizar su satisfacción y gestionar las tandas de donaciones.

Here’s a section you can add to your `README.md` for running the project and setting up the dependencies:

---

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. You can verify it by running the following command:

```bash
python --version
```

If Python is not installed, download and install it from the official [Python website](https://www.python.org/downloads/).

### Setting Up the Environment

1. **Clone the Repository:**

   First, clone this repository to your local machine:

   ```bash
git clone https://github.com/AidFoodMX/AidFoodMX-BE
   ```   ````

2. **Navigate to the Project Directory:**

   Move into the project's root directory:


   ````
```bash
cd AidFoodMX-BE
   ```

```bash
cd aidFoodmx   
   ```


3. **Create and Activate a Virtual Environment (Optional but recommended):**


   - **Create a virtual environment**:
     ```bash
python3 -m venv venv
     ```

   - **Activate the virtual environment**:
     - On Windows:

       venv\Scripts\activate

     - On macOS and Linux:

      source venv/bin/activate


1. **Install Dependencies:**

   After activating the virtual environment, install all required dependencies listed in the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   Additionally, do not forget add the .env



### Running the Project

1. **Start the Flask Application:**

   To run the Flask application, use the following command:

   ```bash
   flask run
   ```

   Alternatively, if the project has a custom `app.py` or `main.py`, you can run it directly:

   ```bash
   python app.py
   ```

2. **Access the API:**

   Once the server is running, you can access the endpoints using the following URL format:

   ```
   http://127.0.0.1:5000/<endpoint>
   ```

   For example:
   ```
   http://127.0.0.1:5000/predict_future_beneficiaries?region=Guadalajara&period=6
   ```

---

This should provide the necessary steps to set up and run the project on a new system. Let me know if you need any adjustments!)

## Ejemplos de uso de los endpoints

# AidFoodMX Backend API

Esta sección describe los endpoints de la API para gestionar inventario y donaciones.

---

### 1. **Update Inventory**

- **Método:** `POST`
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

  **Descripción:** Actualiza el inventario actual agregando las cantidades especificadas de cada categoría de artículos (no perecederos, cereales, frutas y verduras, lácteos y carne).

---

### 2. **Record Donations**

- **Método:** `POST`
- **URL:** `http://127.0.0.1:5000/record_donations`
- **Body Example (JSON):**

  ```json
  {
    "non_perishables": 5,
    "cereals": 2,
    "fruits_vegetables": 7,
    "dairy": 1,
    "meat": 2
  }
  ```

  **Descripción:** Registra las donaciones recibidas y actualiza el conteo de donaciones del mes y la semana según la fecha de la solicitud.

---

### 3. **Get Total Inventory**

- **Método:** `GET`
- **URL:** `http://127.0.0.1:5000/get_total_inventory`
- **Response Example (JSON):**

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

  **Descripción:** Recupera el inventario total actual de cada categoría de artículos (no perecederos, cereales, frutas y verduras, lácteos y carne).

---

### 4. **Get Donations Per Month**

- **Método:** `GET`
- **URL:** `http://127.0.0.1:5000/get_donations_per_month`
- **Response Example (JSON):**

  ```json
    {
       "donations_per_month": {
           "2024-01": 5,
           "2024-02": 5,
           "2024-03": 5,
           "2024-04": 1,
           "2024-05": 1,
           "2024-06": 1,
           "2024-07": 1,
           "2024-08": 1,
           "2024-09": 1,
           "2024-10": 5,
           "2024-11": 0,
           "2024-12": 0
       }
   }
  ```

  **Descripción:** Devuelve las donaciones totales recibidas para cada categoría por mes.

---



### 5. **Get Donations Per Month**

- **Método:** `GET`
- URL: http://127.0.0.1:5000/donations/kind-of-donations-per-month
- **Response Example (JSON):**

  ```json
  {
  "donations_per_month": {
    "2024-01": {
      "non_perishables": 30,
      "cereals": 15,
      "fruits_vegetables": 10,
      "dairy": 5,
      "meat": 2
    },
    "2024-02": {
      "non_perishables": 20,
      "cereals": 10,
      "fruits_vegetables": 8,
      "dairy": 4,
      "meat": 1
    }
  }
}
  ```

  **Descripción:** Devuelve las donaciones totales recibidas para cada categoría por mes.

---

### 6. **Get Donations Per Week**

- **Método:** `GET`
- URL: http://127.0.0.1:5000/donations/per-week
- **Response Example (JSON):**

  ```json
[
  {
    "donation_date": "2024-10-10T15:30:00",
    "non_perishables": 5,
    "cereals": 3,
    "fruits_vegetables": 4,
    "dairy": 2,
    "meat": 1,
    "donator": "Donator A",
    "region": "Region 1"
  }
]
  ```

  **Descripción:** Devuelve las donaciones recibidas por semana (número de semana basado en el año).

---

*  Get Top Donators Per Region

	•	Método: GET
	•	URL: http://127.0.0.1:5000/donations/top-donators/Guadalajara
	•	Response Example (JSON):

  example output: 
  {
    "donations_per_week": [
        {
            "cereals": 70,
            "dairy": 90,
            "donation_date": "2024-10-08T10:05:00",
            "donator": "Bodega Aurrera",
            "fruits_vegetables": 140,
            "meat": 50,
            "non_perishables": 150,
            "region": "Guadalajara"
        },
        {
            "cereals": 60,
            "dairy": 50,
            "donation_date": "2024-10-09T16:30:00",
            "donator": "Soriana",
            "fruits_vegetables": 120,
            "meat": 30,
            "non_perishables": 100,
            "region": "Tijuana"
        },
        {
            "cereals": 70,
            "dairy": 60,
            "donation_date": "2024-10-10T07:40:00",
            "donator": "Oxxo",
            "fruits_vegetables": 160,
            "meat": 40,
            "non_perishables": 130,
            "region": "Monterrey"
        },
        {
            "cereals": 90,
            "dairy": 100,
            "donation_date": "2024-10-11T12:45:00",
            "donator": "Walmart",
            "fruits_vegetables": 180,
            "meat": 70,
            "non_perishables": 160,
            "region": "Guadalajara"
        },
        {
            "cereals": 80,
            "dairy": 110,
            "donation_date": "2024-10-12T09:20:00",
            "donator": "Ley",
            "fruits_vegetables": 130,
            "meat": 50,
            "non_perishables": 140,
            "region": "Tijuana"
        },
        {
            "cereals": 100,
            "dairy": 130,
            "donation_date": "2024-10-13T08:00:00",
            "donator": "Bodega Aurrera",
            "fruits_vegetables": 200,
            "meat": 60,
            "non_perishables": 180,
            "region": "Monterrey"
        },
        {
            "cereals": 70,
            "dairy": 90,
            "donation_date": "2024-10-08T10:05:00",
            "donator": "Bodega Aurrera",
            "fruits_vegetables": 140,
            "meat": 50,
            "non_perishables": 150,
            "region": "Guadalajara"
        },
        {
            "cereals": 60,
            "dairy": 50,
            "donation_date": "2024-10-09T16:30:00",
            "donator": "Soriana",
            "fruits_vegetables": 120,
            "meat": 30,
            "non_perishables": 100,
            "region": "Tijuana"
        },
        {
            "cereals": 70,
            "dairy": 60,
            "donation_date": "2024-10-10T07:40:00",
            "donator": "Oxxo",
            "fruits_vegetables": 160,
            "meat": 40,
            "non_perishables": 130,
            "region": "Monterrey"
        },
        {
            "cereals": 90,
            "dairy": 100,
            "donation_date": "2024-10-11T12:45:00",
            "donator": "Walmart",
            "fruits_vegetables": 180,
            "meat": 70,
            "non_perishables": 160,
            "region": "Guadalajara"
        },
        {
            "cereals": 80,
            "dairy": 110,
            "donation_date": "2024-10-12T09:20:00",
            "donator": "Ley",
            "fruits_vegetables": 130,
            "meat": 50,
            "non_perishables": 140,
            "region": "Tijuana"
        },
        {
            "cereals": 100,
            "dairy": 130,
            "donation_date": "2024-10-13T08:00:00",
            "donator": "Bodega Aurrera",
            "fruits_vegetables": 200,
            "meat": 60,
            "non_perishables": 180,
            "region": "Monterrey"
        },
        {
            "cereals": 70,
            "dairy": 90,
            "donation_date": "2024-10-08T10:05:00",
            "donator": "Bodega Aurrera",
            "fruits_vegetables": 140,
            "meat": 50,
            "non_perishables": 150,
            "region": "Guadalajara"
        },
        {
            "cereals": 60,
            "dairy": 50,
            "donation_date": "2024-10-09T16:30:00",
            "donator": "Soriana",
            "fruits_vegetables": 120,
            "meat": 30,
            "non_perishables": 100,
            "region": "Tijuana"
        },
        {
            "cereals": 70,
            "dairy": 60,
            "donation_date": "2024-10-10T07:40:00",
            "donator": "Oxxo",
            "fruits_vegetables": 160,
            "meat": 40,
            "non_perishables": 130,
            "region": "Monterrey"
        },
        {
            "cereals": 90,
            "dairy": 100,
            "donation_date": "2024-10-11T12:45:00",
            "donator": "Walmart",
            "fruits_vegetables": 180,
            "meat": 70,
            "non_perishables": 160,
            "region": "Guadalajara"
        },
        {
            "cereals": 80,
            "dairy": 110,
            "donation_date": "2024-10-12T09:20:00",
            "donator": "Ley",
            "fruits_vegetables": 130,
            "meat": 50,
            "non_perishables": 140,
            "region": "Tijuana"
        },
        {
            "cereals": 100,
            "dairy": 130,
            "donation_date": "2024-10-13T08:00:00",
            "donator": "Bodega Aurrera",
            "fruits_vegetables": 200,
            "meat": 60,
            "non_perishables": 180,
            "region": "Monterrey"
        },
        {
            "cereals": 70,
            "dairy": 90,
            "donation_date": "2024-10-08T10:05:00",
            "donator": "Bodega Aurrera",
            "fruits_vegetables": 140,
            "meat": 50,
            "non_perishables": 150,
            "region": "Guadalajara"
        },
        {
            "cereals": 60,
            "dairy": 50,
            "donation_date": "2024-10-09T16:30:00",
            "donator": "Soriana",
            "fruits_vegetables": 120,
            "meat": 30,
            "non_perishables": 100,
            "region": "Tijuana"
        },
        {
            "cereals": 70,
            "dairy": 60,
            "donation_date": "2024-10-10T07:40:00",
            "donator": "Oxxo",
            "fruits_vegetables": 160,
            "meat": 40,
            "non_perishables": 130,
            "region": "Monterrey"
        },
        {
            "cereals": 90,
            "dairy": 100,
            "donation_date": "2024-10-11T12:45:00",
            "donator": "Walmart",
            "fruits_vegetables": 180,
            "meat": 70,
            "non_perishables": 160,
            "region": "Guadalajara"
        },
        {
            "cereals": 80,
            "dairy": 110,
            "donation_date": "2024-10-12T09:20:00",
            "donator": "Ley",
            "fruits_vegetables": 130,
            "meat": 50,
            "non_perishables": 140,
            "region": "Tijuana"
        },
        {
            "cereals": 100,
            "dairy": 130,
            "donation_date": "2024-10-13T08:00:00",
            "donator": "Bodega Aurrera",
            "fruits_vegetables": 200,
            "meat": 60,
            "non_perishables": 180,
            "region": "Monterrey"
        }
    ]
}


## **here we get the top global donators** 

- **URL:**  http://127.0.0.1:5000/donations/top-donators-global

example output: 

{
    "top_donators_global": [
        {
            "donator": "Soriana",
            "total": 16
        },
        {
            "donator": "Walmart",
            "total": 16
        },
        {
            "donator": "Bodega Aurrera",
            "total": 16
        },
        {
            "donator": "Ley",
            "total": 16
        },
        {
            "donator": "Oxxo",
            "total": 16
        }
    ]
}

### **Recordar múltiples donaciones**


- **URL:** `http://127.0.0.1:5000/record_multiple_donations`
- **Body Example (JSON):**

  ```json
[
  {
    "donation_date": "2024-10-01T10:00:00",
    "non_perishables": 150,
    "cereals": 80,
    "fruits_vegetables": 200,
    "dairy": 100,
    "meat": 50,
    "donator": "Walmart",
    "region": "Guadalajara"
  },
  {
    "donation_date": "2024-10-02T11:30:00",
    "non_perishables": 120,
    "cereals": 70,
    "fruits_vegetables": 90,
    "dairy": 50,
    "meat": 30,
    "donator": "Ley",
    "region": "Tijuana"
  },
  {
    "donation_date": "2024-10-03T12:00:00",
    "non_perishables": 200,
    "cereals": 90,
    "fruits_vegetables": 180,
    "dairy": 110,
    "meat": 40,
    "donator": "Bodega Aurrera",
    "region": "Monterrey"
  },
  {
    "donation_date": "2024-10-04T09:45:00",
    "non_perishables": 130,
    "cereals": 60,
    "fruits_vegetables": 140,
    "dairy": 80,
    "meat": 60,
    "donator": "Soriana",
    "region": "Guadalajara"
  },
  {
    "donation_date": "2024-10-05T14:15:00",
    "non_perishables": 90,
    "cereals": 50,
    "fruits_vegetables": 120,
    "dairy": 70,
    "meat": 40,
    "donator": "Oxxo",
    "region": "Tijuana"
  },
  {
    "donation_date": "2024-10-06T08:30:00",
    "non_perishables": 110,
    "cereals": 60,
    "fruits_vegetables": 150,
    "dairy": 100,
    "meat": 20,
    "donator": "Walmart",
    "region": "Cancún"
  },
  {
    "donation_date": "2024-10-07T13:20:00",
    "non_perishables": 170,
    "cereals": 80,
    "fruits_vegetables": 200,
    "dairy": 130,
    "meat": 60,
    "donator": "Ley",
    "region": "Monterrey"
  },
  {
    "donation_date": "2024-10-08T10:05:00",
    "non_perishables": 150,
    "cereals": 70,
    "fruits_vegetables": 140,
    "dairy": 90,
    "meat": 50,
    "donator": "Bodega Aurrera",
    "region": "Guadalajara"
  },
  {
    "donation_date": "2024-10-09T16:30:00",
    "non_perishables": 100,
    "cereals": 60,
    "fruits_vegetables": 120,
    "dairy": 50,
    "meat": 30,
    "donator": "Soriana",
    "region": "Tijuana"
  },
  {
    "donation_date": "2024-10-10T07:40:00",
    "non_perishables": 130,
    "cereals": 70,
    "fruits_vegetables": 160,
    "dairy": 60,
    "meat": 40,
    "donator": "Oxxo",
    "region": "Monterrey"
  },
  {
    "donation_date": "2024-10-11T12:45:00",
    "non_perishables": 160,
    "cereals": 90,
    "fruits_vegetables": 180,
    "dairy": 100,
    "meat": 70,
    "donator": "Walmart",
    "region": "Guadalajara"
  },
  {
    "donation_date": "2024-10-12T09:20:00",
    "non_perishables": 140,
    "cereals": 80,
    "fruits_vegetables": 130,
    "dairy": 110,
    "meat": 50,
    "donator": "Ley",
    "region": "Tijuana"
  },
  {
    "donation_date": "2024-10-13T08:00:00",
    "non_perishables": 180,
    "cereals": 100,
    "fruits_vegetables": 200,
    "dairy": 130,
    "meat": 60,
    "donator": "Bodega Aurrera",
    "region": "Monterrey"
  },
  {
    "donation_date": "2024-10-14T14:50:00",
    "non_perishables": 110,
    "cereals": 60,
    "fruits_vegetables": 150,
    "dairy": 90,
    "meat": 40,
    "donator": "Soriana",
    "region": "Guadalajara"
  },
  {
    "donation_date": "2024-10-15T13:00:00",
    "non_perishables": 120,
    "cereals": 70,
    "fruits_vegetables": 140,
    "dairy": 80,
    "meat": 50,
    "donator": "Oxxo",
    "region": "Tijuana"
  },
  {
    "donation_date": "2024-10-16T11:15:00",
    "non_perishables": 160,
    "cereals": 90,
    "fruits_vegetables": 170,
    "dairy": 100,
    "meat": 60,
    "donator": "Walmart",
    "region": "Cancún"
  },
  {
    "donation_date": "2024-10-17T10:30:00",
    "non_perishables": 130,
    "cereals": 80,
    "fruits_vegetables": 130,
    "dairy": 90,
    "meat": 50,
    "donator": "Ley",
    "region": "Monterrey"
  },
  {
    "donation_date": "2024-10-18T12:10:00",
    "non_perishables": 140,
    "cereals": 70,
    "fruits_vegetables": 150,
    "dairy": 110,
    "meat": 40,
    "donator": "Bodega Aurrera",
    "region": "Guadalajara"
  },
  {
    "donation_date": "2024-10-19T14:00:00",
    "non_perishables": 150,
    "cereals": 90,
    "fruits_vegetables": 170,
    "dairy": 120,
    "meat": 60,
    "donator": "Soriana",
    "region": "Tijuana"
  },
  {
    "donation_date": "2024-10-20T11:35:00",
    "non_perishables": 120,
    "cereals": 60,
    "fruits_vegetables": 160,
    "dairy": 100,
    "meat": 40,
    "donator": "Oxxo",
    "region": "Monterrey"
  }
]
  ```

  **Descripción:** Registra múltiples donaciones con una sola solicitud.

---

### **Registrar Beneficiarios**

#### **Registrar un beneficiario individual**

- **URL:** `http://127.0.0.1:5000/register_beneficiary_with_region`
- **Body Example (JSON):**

  ```json
  {
    "name": "María López",
    "satisfaction": 4,
    "date": "2024-02-15",
    "region": "Querétaro"
  }
  ```

---

#### **Registrar múltiples beneficiarios**

- **URL:** `http://127.0.0.1:5000/register_multiple_beneficiaries`
- **Body Example (JSON):**

  ```json
  [
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
  ```

---

### **Obtener información de beneficiarios**

#### **Número de beneficiarios por día**

- **URL:** `http://127.0.0.1:5000/get_beneficiaries_per_day`

#### **Número de beneficiarios por mes**

- **URL:** `http://127.0.0.1:5000/get_beneficiaries_per_month`

---

### **Registrar ranking de paquetes de alimentos**

- **URL:** `http://127.0.0.1:5000/register_food_package_ranking`
- **Body Example (JSON):**

  ```json
  {
    "info": "Package S",
    "date": "2024-09-19",
    "satisfaction": 5
  }
  ```

#### **Registrar múltiples rankings de paquetes de alimentos**

- **URL:** `http://127.0.0.1:5000/register_multiple_food_package_rankings`
- **Body Example (JSON):**

  ```json
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
  ```

---

### **Obtener ranking de paquetes por mes**

- **URL:** `http://127.0.0.1:5000/get_food_package_rankings_per_month`
- **Response Example (JSON):**

  ```json
  {
    "data": {
      "2024-10": {
        "Package A": 5.0,
        "Package B": 4.0,
        "Package C": 3.0,
        "Package D": 5.0,
        "Package E": 2.0,
        "Package F": 4.0
      }
    }
  }
  ```

---

### **Predecir futuros beneficiarios** (`predict_future_beneficiaries`)

- **URL:** `http://127.0.0.1:5000/predict_future_beneficiaries?region=Guadalajara&period=6`
  
  **Explanation:**  
  This endpoint generates a prediction of how many beneficiaries a region is likely to register over a specified future period (e.g., 6 months). Based on historical data for the selected region (in this case, "Guadalajara"), it calculates growth trends and projects future numbers. This is particularly useful for forecasting needs, allocating resources, and planning ahead to ensure there are enough food supplies and aid for the anticipated number of beneficiaries.

  **Why it’s useful:**  
  The predictions generated by this endpoint allow organizations to prepare in advance and ensure there is no shortage of resources for future beneficiaries. This helps improve operational efficiency and long-term planning.

---

### **Obtener tendencias de beneficiarios por región** (`get_beneficiary_trends_by_region`)

- **URL:** `http://127.0.0.1:5000/get_beneficiary_trends_by_region?region=Guadalajara&start_date=2024-01-01&end_date=2024-12-31`
  
  **Explanation:**  
  This endpoint retrieves the number of beneficiaries registered per month over a given time range for a specific region. In this example, it shows how many beneficiaries were registered in Guadalajara between January 1, 2024, and December 31, 2024. It aggregates the data on a monthly basis, allowing users to analyze trends and see which months had higher or lower beneficiary registrations.

  **Why it’s useful:**  
  Understanding historical trends helps organizations to identify patterns in demand for assistance across different times of the year. This enables them to be better prepared during peak months when more people may need aid and can also inform strategic decisions, such as increasing outreach in underperforming months.

---


Here is a section you can add to your README file to explain how to use the new /generate_insights endpoint:

Generate Insights Endpoint

Overview

The /generate_insights endpoint leverages the data from beneficiary trends, donation patterns, current inventory status, and food package satisfaction rankings to provide short, valuable insights into the current state and future trends for a specific region. This information can help the organization make data-driven decisions and optimize resources in various regions.

How to Use the Endpoint

Endpoint URL: http://127.0.0.1:5000/generate_insights

Method: POST

Request Body:
This endpoint expects a JSON object with the following structure:

{
    "region": "Guadalajara"
}

	•	region (required): The region for which you want to generate insights. Example: "Guadalajara".

Example Request

Here’s how you would call this endpoint in Postman or similar tools:

POST: http://127.0.0.1:5000/generate_insights

Request Body:

{
    "region": "Guadalajara"
}

Example Response

On a successful request, the response will be a JSON object containing a set of insights related to the specified region:

{
    "message": "Insights generados",
    "insights": {
        "insights": [
            {"punto": "Aumento del 10% en beneficiarios en los últimos 3 meses en la región."},
            {"punto": "Donaciones de cereales estables, pero frutas y verduras han disminuido."},
            {"punto": "Inventario de productos lácteos en niveles críticos."},
            {"punto": "Satisfacción con los paquetes de alimentos ha mejorado en un 15%."}
        ]
    }
}

Type of Information You Can Obtain

The insights generated by the Gemini API provide a short, bullet-point summary of the most relevant information based on the data from the region. Here are the key types of insights:

	1.	Beneficiary Trends: How the number of beneficiaries has changed over the past year, showing any increases or decreases in certain periods.
	2.	Donation Patterns: Insights into what types of donations are more common and whether any particular type of food donation is increasing or decreasing.
	3.	Inventory Levels: Critical information about the stock levels of different food categories, allowing the organization to assess what is in abundance or what is running low.
	4.	Satisfaction Rankings: A measure of how satisfied beneficiaries are with the food packages they receive, helping to optimize and adjust the content of food packages to improve satisfaction.

These insights will help guide decisions about resource allocation, food donation campaigns, and beneficiary support strategies for the specified region.

Error Handling

If the request is not properly formed or there is a failure in generating insights, the API will respond with an error message in JSON format like this:

{
    "message": "Error al generar insights",
    "error": "Descripción del error"
}

Conclusion

By calling the /generate_insights endpoint, you can easily obtain concise, actionable insights based on historical data and current trends, helping the organization to make informed decisions and improve the effectiveness of its operations in different regions.

This explanation provides a clear overview of how to use the endpoint, what kind of data you can expect, and the value the endpoint provides.

Here’s the explanation in markdown format:

## Generate Insights Endpoint

### Overview
The `/generate_insights` endpoint provides short,  insights based on beneficiary trends, donation patterns, inventory levels, and food package satisfaction rankings for a specific region. These insights help guide decisions on resource allocation, beneficiary support and general bussines knowledge. 

### How to Use
**Endpoint URL**: `http://127.0.0.1:5000/generate_insights`

**Method**: POST

**Request Body**:
```json
{
    "region": "Guadalajara"
}

Example Response

{
    "message": "Insights generados",
    "insights": {
        "insights": [
            {"punto": "Aumento del 10% en beneficiarios en los últimos 3 meses."},
            {"punto": "Donaciones de frutas y verduras han disminuido."},
            {"punto": "Inventario de lácteos en niveles críticos."},
            {"punto": "Mejora del 15% en satisfacción con los paquetes de alimentos."}
        ]
    }
}
```

Insights Provided

	•	Beneficiary trends over the past year.
	•	Donation patterns by food type.
	•	Current inventory levels and critical shortages.
	•	Satisfaction rankings for food packages.

This endpoint allows for quick, data-driven insights to improve decision-making for resource management.



Get All Regions Endpoint

This endpoint retrieves all distinct regions from the beneficiaries table. It is useful for obtaining a clean list of regions where beneficiaries are registered.

Endpoint:

	•	URL: /get_regions
	•	Method: GET

Example Usage in Postman:

	•	Select GET method.
	•	Enter the URL: http://<your-server>/get_regions
	•	Send the request.

Example Response:

{
    "message": "Regions retrieved",
    "regions": ["Guadalajara", "Monterrey", "Mexico City"]
}

This provides a clean list of regions available in the system.