from flask import request, jsonify
from .models import Beneficiary
from .services import register_beneficiary_service, get_beneficiaries_service

def register_routes(app):
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to AidfoodMx Backend!"})

    # Ruta POST para agregar un beneficiario
    @app.route('/register_beneficiary', methods=['POST'])
    def register_beneficiary():
        data = request.json
        new_beneficiary = register_beneficiary_service(data)
        return jsonify({"message": "Beneficiary registered", "data": new_beneficiary.__dict__}), 201

    # Ruta GET para obtener el número de beneficiarios
    @app.route('/get_beneficiaries', methods=['GET'])
    def get_beneficiaries():
        data_for_chart = get_beneficiaries_service()
        return jsonify({"data": data_for_chart}), 200
