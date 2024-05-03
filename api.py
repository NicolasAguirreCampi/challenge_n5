from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db
from models import Officer, Vehicle, Infraction
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/login', methods=['POST'])
def login():
    name = request.json.get('name', None)
    password = request.json.get('password', None)
    officer = Officer.query.filter_by(name=name).first()
    if officer and officer.check_password(password):
        access_token = create_access_token(identity=name)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad name or password"}), 401

@api_bp.route('/cargar_infraccion', methods=['POST'])
@jwt_required()
def cargar_infraccion():
    try:
        current_user = get_jwt_identity()

        data = request.json
        license_plate = data['placa_patente']
        timestamp = data['timestamp']
        comments = data['comentarios']

        try:
            parsed_timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
        except ValueError: # Error de formato de timestamp
            return jsonify({'error': 'Invalid timestamp format. Use YYYY-MM-DDTHH:MM:SS'}), 400

        vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404

        new_infraction = Infraction(
            license_plate=vehicle.license_plate,
            timestamp=parsed_timestamp,
            comments=comments
        )
        db.session.add(new_infraction)
        db.session.commit()

        return jsonify({'message': 'Infraction registered successfully'}), 200
    except KeyError: # Error de request
        return jsonify({'error': 'Malformed request, missing necessary fields'}), 400

    except SQLAlchemyError as e: # Errores de db
        db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 500

    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

@api_bp.route('/hola_world', methods=['GET'])
@jwt_required()
def hello_world():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
