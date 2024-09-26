from flask import request, jsonify
from .services import register_beneficiary_with_date, get_beneficiaries_per_month, get_beneficiaries_per_day

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
