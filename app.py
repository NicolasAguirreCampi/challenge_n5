from datetime import datetime
from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from database import db
from models import Person, Vehicle, Officer, Infraction
from api import api_bp
from admin import admin_bp

# db seeds para testing
def seed_database():
    # Empezar la db en limpio
    db.drop_all()
    db.create_all()

    # Officer
    officer1 = Officer(name="Ryan", unique_id="OFF123")
    officer1.set_password("ryan_password")

    officer2 = Officer(name="Sara", unique_id="OFF456")
    officer2.set_password("sara_password")
    db.session.add_all([officer1, officer2])

    # Person
    person1 = Person(name="John Doe", email="john.doe@example.com")
    person2 = Person(name="Jane Smith", email="jane.smith@example.com")
    db.session.add_all([person1, person2])

    # Vehicle
    vehicle1 = Vehicle(license_plate="ABC123", brand="Toyota", color="Red", owner=person1)
    vehicle2 = Vehicle(license_plate="XYZ789", brand="Honda", color="Blue", owner=person2)
    db.session.add_all([vehicle1, vehicle2])

    # Infraction
    infraction1 = Infraction(license_plate=vehicle1.license_plate, timestamp=datetime.now(), comments="Speeding")
    infraction2 = Infraction(license_plate=vehicle2.license_plate, timestamp=datetime.now(), comments="Parking violation")
    db.session.add_all([infraction1, infraction2])

    db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # JWT config
    app.config['JWT_SECRET_KEY'] = 'clave_json_web_token'
    app.secret_key = "clave" # Configuracion necesaria para la sesion de web (para uso de mensajes flash)
    jwt = JWTManager(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Descomentar para seed (limpia la db y carga datos de prueba)
        seed_database()

    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
