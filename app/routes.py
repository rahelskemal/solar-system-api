from app import db
from models.planet import Planet 
from flask import Blueprint, jsonify, abort, request, make_response

# HELPER FUNCTIONS #

def validate_planet(planet_id): 
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"{planet_id} is invalid"}, 400))
    
    planet = Planet.query.get(planet_id)

    if not planet:
        abort(make_response({"message": f"planet {planet_id} not found"}, 404))

    return planet

# ROUTE FUNCTIONS # 

planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    if "name" not in request_body or "description" not in request_body or "moon_count" not in request_body:
        return make_response("Invalid Request", 400)

        
    new_planet = Planet.from_dict(request_body)
    db.session.add(new_planet)
    db.session.commit()
    return make_response(f" Planet {new_planet.name} sucessfully created", 201)

@planets_bp.route("", methods=["GET"])
def get_all_planets():
    name_query = request.args.get("name")
    moon_count_query = request.args.get("moon_count")

    if name_query:
        all_planets = Planet.query.filter_by(name=name_query)
    elif moon_count_query:
        all_planets = Planet.query.filter_by(moon_count=moon_count_query)
    else:
        all_planets = Planet.query.all()

    return jsonify([planet.to_dict() for planet in all_planets]), 200

@planets_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()


    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.moon_count = request_body["moon_count"]

    db.session.commit()
    return make_response(f"Planet {planet.id} successfully updated")

@planets_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return planet.to_dict()

@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)
    
    db.session.delete(planet)
    db.session.commit()

    return make_response(f"Planet #{planet.id} successfully deleted")
