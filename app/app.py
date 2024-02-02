#!/usr/bin/env python3
from flask_cors import CORS
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/simon/Flask/wk1_code _challenge/python-code-challenge-superheroes/code-challenge/app/db/app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
CORS(app)
migrate = Migrate(app, db)

@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes_list = []
    for hero in Hero.query.all():
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
        }
        heroes_list.append(hero_dict)
    response = make_response(jsonify(heroes_list), 200)
    return response

@app.route("/heroes/<int:id>")
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
        }
        response = make_response(jsonify(hero_dict), 200)
    else:
        response = make_response(jsonify({"error": "Hero not found"}), 404)
    return response

@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    power_list = []
    for power in powers:
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        power_list.append(power_dict)
    response = make_response(jsonify(power_list), 200)
    return response

@app.route("/powers/<int:id>")
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        response = make_response(jsonify(power_dict), 200)
    else:
        response = make_response(jsonify({"error": "Power not found"}), 404)
    return response

@app.route("/powers/<int:id>", methods=["PATCH"])
def patch_power(id):
    power = Power.query.get(id)
    if not power:
        return make_response(jsonify({"error": "Power not found"}), 404)

    description = request.json.get("description")
    if not description:
        return make_response(jsonify({"error": "Validation error: Description is required"}), 400)

    power.description = description
    db.session.commit()

    updated_power_dict = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }

    return jsonify(updated_power_dict)

@app.route("/hero_powers", methods=["POST"])
def post_hero_powers():
    strength = request.form.get("strength")
    power_id = request.form.get("power_id")
    hero_id = request.form.get("hero_id")

    new_hero_power = Hero(strength=strength, power_id=power_id, hero_id=hero_id)
    db.session.add(new_hero_power)
    db.session.commit()

    hero_power_dict = {
        "id": new_hero_power.id,
        "strength": new_hero_power.strength,
        "power_id": new_hero_power.power_id,
        "hero_id": new_hero_power.hero_id
    }

    response = make_response(jsonify(hero_power_dict), 201)
    return response

if __name__ == "__main__":
    app.run(port=5555, debug=True)
