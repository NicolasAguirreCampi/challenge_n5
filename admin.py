from flask import request, Blueprint, jsonify, render_template, flash, redirect, url_for
from models import Person, Vehicle, Officer
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
        return jsonify({'error': 'Person not found'}), 404
    
    db.session.delete(person)
    db.session.commit()

    return redirect(url_for('admin.get_people'))

# # VEHICULOS
# @admin_bp.route('/vehicles', methods=['GET'])
# def get_vehicles():
#     vehicles = Vehicle.query.all()
#     return jsonify([vehicle.to_dict() for vehicle in vehicles]), 200

# # OFICIALES
# @admin_bp.route('/officers', methods=['GET'])
# def get_officers():
#     officers = Officer.query.all()
#     return jsonify([officer.to_dict() for officer in officers]), 200