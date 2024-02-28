#!/usr/bin/env python3
from flask_cors import CORS
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power,Hero_power

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
CORS(app)
migrate = Migrate(app, db)


@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(heroes_list)

@app.route("/heroes/<int:id>", methods=["GET"])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [{"id": power.id, "name": power.name, "description": power.description} for power in hero.powers]
        }
        return jsonify(hero_dict)
    else:
        return jsonify({"error": "Hero not found"}), 404

@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    power_list = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(power_list)

@app.route("/powers/<int:id>", methods=["GET"])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        return jsonify(power_dict)
    else:
        return jsonify({"error": "Power not found"}), 404

@app.route("/powers/<int:id>", methods=["PATCH"])
def patch_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    description = request.json.get("description")
    if not description:
        return jsonify({"error": "Validation error: Description is required"}), 400

    if len(description) < 20:
        return jsonify({"error": "Validation error: Description must be more than 20 characters long"}), 400

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
    data = request.json
    strength = data.get("strength")
    power_id = data.get("power_id")
    hero_id = data.get("hero_id")

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({"error": "Hero or Power not found"}), 404

    new_hero_power = Hero_power(strength=strength, power_id=power_id, hero_id=hero_id)
    db.session.add(new_hero_power)
    db.session.commit()

    hero_dict = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": [{"id": power.id, "name": power.name, "description": power.description}]
    }

    return jsonify(hero_dict), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)