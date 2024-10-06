
---

# AidfoodMx - Backend

Este es el backend del proyecto **AidfoodMx**, que utiliza Flask para gestionar la lógica y las API que interactúan con los beneficiarios de BAMX. El proyecto permite registrar beneficiarios, analizar su satisfacción y gestionar las tandas de donaciones.

## Requerimientos

Para ejecutar este proyecto localmente, necesitarás tener instalados los siguientes programas:

- **Python 3.8+**
- **pip** (el gestor de paquetes de Python)
- Un entorno virtual de Python (recomendado)

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

  **Descripción:** Devuelve las donaciones totales recibidas para cada categoría por mes.

---

### 5. **Get Donations Per Week**

- **Método:** `GET`
- **URL:** `http://127.0.0.1:5000/get_donations_per_week`
- **Response Example (JSON):**

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

  **Descripción:** Devuelve las donaciones recibidas por semana (número de semana basado en el año).

---

### **Recordar múltiples donaciones**

- **URL:** `http://127.0.0.1:5000/record_multiple_donations`
- **Body Example (JSON):**

  ```json
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

### **Predecir futuros beneficiarios**

- **URL:** `http://127.0.0.1:5000/predict_future_beneficiaries?region=Guadalajara&period=6`
- **Response Example (JSON):**

  ```json
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
  ```

---

### **Obtener tendencias de beneficiarios por región**

- **URL:** `http://127.0.0.1:5000/get_beneficiary_trends_by_region?region=Guadalajara&start_date=2024-01-01&end_date=2024-12-31`
- **Response Example (JSON):**

  ```json
  {
    "message": "Beneficiary trends retrieved",
    "trends": {
      "2024-01": 2,
      "2024-09": 3
    }
  }
  ```

---

