from flask import request, jsonify
from .services import register_beneficiary_with_date, get_beneficiaries_per_month, get_beneficiaries_per_day
from .services import register_food_package_ranking, get_food_package_rankings_per_month

def register_routes(app):
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to AidfoodMx Backend!"})

    # Ruta POST para agregar un beneficiario con fecha
    @app.route('/register_beneficiary_with_date', methods=['POST'])
    def register_beneficiary_with_date_route():
        data = request.json
        new_beneficiary = register_beneficiary_with_date(data)
        return jsonify({"message": "Beneficiary registered with date", "data": new_beneficiary.__dict__}), 201

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
        return jsonify({"message": "Food package ranked", "data": package.__dict__}), 201

    # Ruta GET para obtener el promedio de rankings por paquete mes a mes
    @app.route('/get_food_package_rankings_per_month', methods=['GET'])
    def get_food_package_rankings_per_month_route():
        data = get_food_package_rankings_per_month()
        return jsonify({"data": data}), 200