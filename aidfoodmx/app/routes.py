from flask import request, jsonify
from datetime import datetime, timedelta
from .services import (
    register_beneficiary_with_region, get_beneficiaries_per_month, get_beneficiaries_per_day,
    register_food_package_ranking, get_food_package_rankings_per_month, get_beneficiary_trends_by_region, 
    predict_future_beneficiaries, record_donations, get_total_inventory, 
    get_donations_per_month_of_year, get_donations_per_week, update_inventory, record_multiple_donations, register_multiple_beneficiaries, register_multiple_food_package_rankings,
    get_kind_of_donations_per_month
)

def register_routes(app):
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to AidfoodMx Backend!"})

    # Ruta POST para agregar un beneficiario con región
    @app.route('/register_beneficiary_with_region', methods=['POST'])
    def register_beneficiary_with_region_route():
        data = request.json
        new_beneficiary = register_beneficiary_with_region(data)
        return jsonify({"message": "Beneficiary registered with region", "data": new_beneficiary}), 201

    # Ruta GET para obtener el número de beneficiarios por mes
    @app.route('/get_beneficiaries_per_month', methods=['GET'])
    def get_beneficiaries_per_month_route():
        data = get_beneficiaries_per_month()
        return jsonify({"data": data}), 200

    # Ruta GET para obtener los beneficiarios por día en el mes actual
    @app.route('/get_beneficiaries_per_day', methods=['GET'])
    def get_beneficiaries_per_day_route():
        data = get_beneficiaries_per_day()
        return jsonify({"data": data}), 200

    # Ruta POST para registrar un ranking de paquete de comida
    @app.route('/register_food_package_ranking', methods=['POST'])
    def register_food_package_ranking_route():
        data = request.json
        package = register_food_package_ranking(data)
        return jsonify({"message": "Food package ranked", "data": package}), 201
    
    @app.route('/register_multiple_food_package_rankings', methods=['POST'])
    def register_multiple_food_package_rankings_route():
        try:
            rankings = request.json  # Expecting a list of rankings in the request body
            result = register_multiple_food_package_rankings(rankings)
            return jsonify(result), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Ruta GET para obtener el promedio de rankings por paquete mes a mes
    @app.route('/get_food_package_rankings_per_month', methods=['GET'])
    def get_food_package_rankings_per_month_route():
        data = get_food_package_rankings_per_month()
        return jsonify({"data": data}), 200

    # Ruta GET para obtener tendencias de beneficiarios por región
    # Ejemplo de ruta: "/get_beneficiary_trends_by_region?region=Guadalajara&start_date=2024-01-01&end_date=2024-12-31"
    @app.route('/get_beneficiary_trends_by_region', methods=['GET'])
    def get_beneficiary_trends_by_region_route():
        try:
            # Get the query parameters
            region = request.args.get('region')
            start_date_str = request.args.get('start_date')
            end_date_str = request.args.get('end_date')

            # Validate required parameters
            if not region or not start_date_str or not end_date_str:
                return jsonify({"error": "Missing required parameters: region, start_date, or end_date"}), 400

            # Convert the date strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            # Call the service to get beneficiary trends by region and date range
            trends = get_beneficiary_trends_by_region(region, start_date, end_date)

            return jsonify(trends), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if __name__ == '__main__':
        app.run(debug=True)
    # Ruta GET para predecir el número de beneficiarios en el futuro basado en tendencias pasadas
    # Ejemplo de ruta: "/get_future_beneficiary_predictions?region=Guadalajara&period=3"
    # @app.route('/get_future_beneficiary_predictions', methods=['GET'])
    # def get_future_beneficiary_predictions_route():
    #     region = request.args.get('region')
    #     period = int(request.args.get('period', 3))  # Default a 3 meses
    #     predictions = predict_future_beneficiaries(region, period)
    #     return jsonify({"predictions": predictions}), 200

    @app.route('/predict_future_beneficiaries', methods=['GET'])
    def predict_future_beneficiaries_route():
        region = request.args.get('region')
        period = int(request.args.get('period', 3))  # Default period of 3 months

        if not region:
            return jsonify({"error": "Region is required"}), 400

        result = predict_future_beneficiaries(region, period)
        return jsonify(result), 200
    # Ruta POST para actualizar el inventario
    @app.route('/update_inventory', methods=['POST'])
    def update_inventory_route():
        data = request.json
        updated_inventory = update_inventory(data)
        return jsonify({
            "message": updated_inventory.get("message"),
            "inventory": updated_inventory.get("inventory", {})
        }), 200

    # Ruta POST para registrar las donaciones recibidas
# Ruta POST para registrar las donaciones recibidas
    @app.route('/record_donations', methods=['POST'])
    def record_donations_route():
        data = request.json  # Recibe los datos del cuerpo de la solicitud
        response = record_donations(data)
        return jsonify(response), 200  # Retorna el resultado como JSON

    # Ruta GET para obtener el inventario total actual
    @app.route('/get_total_inventory', methods=['GET'])
    def get_total_inventory_route():
        total_inventory = get_total_inventory()
        return jsonify(total_inventory), 200

    # Ruta GET para obtener las donaciones por mes
    @app.route('/get_donations_per_month', methods=['GET'])
    def get_donations_per_month_route():
        donations_per_month = get_donations_per_month_of_year()
        return jsonify({"donations_per_month": donations_per_month}), 200

    # Ruta GET para obtener las donaciones por semana
    @app.route('/get_donations_per_week', methods=['GET'])
    def get_donations_per_week_route():
        donations_per_week = get_donations_per_week()
        return jsonify({"donations_per_week": donations_per_week}), 200
    
        # Ruta POST para registrar múltiples donaciones con fechas pasadas
    @app.route('/record_multiple_donations', methods=['POST'])
    def record_multiple_donations_route():
        data = request.json  # Esperamos una lista de donaciones
        response = record_multiple_donations(data)
        return jsonify(response), 201
    @app.route('/get_kind_of_donations_per_month', methods=['GET'])
    def get_kind_of_donations_per_month_route():
        data = get_kind_of_donations_per_month()
        return jsonify(data), 200
        
       
    # Ruta POST para registrar múltiples beneficiarios
    @app.route('/register_multiple_beneficiaries', methods=['POST'])
    def register_multiple_beneficiaries_route():
        beneficiaries = request.json  # Expecting a list of beneficiaries in JSON format
        result = register_multiple_beneficiaries(beneficiaries)
        return jsonify(result), 201