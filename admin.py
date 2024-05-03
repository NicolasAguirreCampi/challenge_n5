from flask import request, Blueprint, jsonify, render_template, flash, redirect, url_for
from models import Person, Vehicle, Officer, Infraction
from database import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET'])
def admin():
    return render_template('home.html')

# PERSONAS
@admin_bp.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    return render_template('people.html', people=people)

@admin_bp.route('/add_person', methods=['GET', 'POST'])
def create_person():
    if request.method == "POST":
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            if not name or not email:
                flash('El nombre y el correo electrónico son obligatorios.', 'error')
            else:
                new_person = Person(name=name, email=email)
                db.session.add(new_person)
                db.session.commit()
                flash('Persona añadida con éxito.', 'success')
                return redirect(url_for('admin.get_people'))
        except Exception as e:
            flash(f'Error. {str(e)}', 'error')
        
    return render_template('add_person.html')

@admin_bp.route('/edit_person/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    person = Person.query.get_or_404(id)
    if request.method == 'POST':
        person.name = request.form['name']
        person.email = request.form['email']
        db.session.commit()
        flash('Información actualizada correctamente', 'success')
        return redirect(url_for('admin.get_people'))
    
    return render_template('edit_person.html', person=person)

@admin_bp.route('/people/<int:id>', methods=['POST'])
def delete_person(id):
    person = Person.query.get(id)

    if person.vehicles:
        flash('No se puede eliminar la persona porque tiene vehículos asociados.', 'error')
        return redirect(url_for('admin.get_people'))

    if not person:
        flash('La persona no existe.', 'error')
        return redirect(url_for('admin.get_people'))
    
    db.session.delete(person)
    db.session.commit()

    return redirect(url_for('admin.get_people'))

# VEHICULOS
@admin_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return render_template('vehicles.html', vehicles=vehicles)

@admin_bp.route('/add_vehicle', methods=['GET', 'POST'])
def create_vehicle():
    if request.method == "POST":
        try:
            license_plate = request.form.get('license_plate')
            brand = request.form.get('brand')
            color = request.form.get('color')
            if not license_plate or not color:
                flash('El nombre y el correo electrónico son obligatorios.', 'error')
            else:
                new_vehicle = Vehicle(license_plate=license_plate, color=color, brand=brand, owner_id=request.form.get('person_id'))
                db.session.add(new_vehicle)
                db.session.commit()
                flash('vehiclea añadida con éxito.', 'success')
                return redirect(url_for('admin.get_vehicle'))
        except Exception as e:
            flash(f'Error. {str(e)}', 'error')
        
    people = Person.query.all()

    return render_template('add_vehicle.html', people=people)

@admin_bp.route('/edit_vehicle/<int:id>', methods=['GET', 'POST'])
def edit_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    people = Person.query.all()

    if request.method == 'POST':
        if vehicle.license_plate != request.form['license_plate']: # Si se edita la patente entonces, verificar que no exista el nuevo valor
            other_vehicle = Vehicle.query.filter_by(license_plate=request.form['license_plate']).first()
            if other_vehicle:
                flash('La patente nueva para el vehiculo ya existe.', 'error')
                return render_template('edit_vehicle.html', vehicle=vehicle, people=people)

        vehicle.license_plate = request.form['license_plate']
        vehicle.brand = request.form['brand']
        vehicle.color = request.form['color']
        person_id = request.form.get('person_id')
        vehicle.owner_id = person_id
        db.session.commit()
        flash('Vehículo actualizado correctamente', 'success')
        return redirect(url_for('admin.get_vehicles'))
    
    return render_template('edit_vehicle.html', vehicle=vehicle, people=people)

@admin_bp.route('/vehicle/<int:id>', methods=['POST'])
def delete_vehicle(id):
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        flash('El vehiculo no existe.', 'error')
        return redirect(url_for('admin.get_vehicles'))
    
    infraction = Infraction.query.filter_by(license_plate=vehicle.license_plate).first()

    if infraction:
        flash('No se puede eliminar vehiculo porque tiene una infraccion.', 'error')
        return redirect(url_for('admin.get_vehicles'))

    db.session.delete(vehicle)
    db.session.commit()

    return redirect(url_for('admin.get_vehicles'))

# # OFICIALES
# @admin_bp.route('/officers', methods=['GET'])
# def get_officers():
#     officers = Officer.query.all()
#     return jsonify([officer.to_dict() for officer in officers]), 200