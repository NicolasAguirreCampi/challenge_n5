from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db
from models import Officer, Vehicle, Infraction, Person

bp = Blueprint('api', __name__)

@bp.route('/login', methods=['POST'])
def login():
    name = request.json.get('name', None)
    password = request.json.get('password', None)
    officer = Officer.query.filter_by(name=name).first()
    if officer and officer.check_password(password):
        access_token = create_access_token(identity=name)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad name or password"}), 401

@bp.route('/cargar_infraccion', methods=['POST'])
@jwt_required()
def cargar_infraccion():
    current_user = get_jwt_identity()

    data = request.json
    vehicle = Vehicle.query.filter_by(license_plate=data['placa_patente']).first()
    if not vehicle:
        
        return jsonify({'error': 'Vehicle not found'}), 404

    new_infraction = Infraction(
        license_plate=vehicle.license_plate,
        timestamp=data['timestamp'],
        comments=data['comentarios']
    )
    db.session.add(new_infraction)
    db.session.commit()

    return jsonify({'message': 'Infraction registered successfully'}), 200

@bp.route('/hola_world', methods=['GET'])
@jwt_required()
def hello_world():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
