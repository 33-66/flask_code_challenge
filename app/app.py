from flask_cors import CORS
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
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
            "powers": [{"id": power.id, "name": power.name, "description": power.description} for power in hero.powers]
        }
        heroes_list.append(hero_dict)
    return jsonify(heroes_list)

@app.route("/heroes/<int:id>")
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
    power_list = []
    for power in powers:
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        power_list.append(power_dict)
    return jsonify(power_list)

@app.route("/powers/<int:id>")
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description,
            "heroes": [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in power.heroes]
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
    strength = request.json.get("strength")
    power_id = request.json.get("power_id")
    hero_id = request.json.get("hero_id")

    if not all([strength, power_id, hero_id]):
        return jsonify({"errors": ["Validation errors: strength, power_id, and hero_id are required"]}), 400

    new_hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
    db.session.add(new_hero_power)
    db.session.commit()

    hero = Hero.query.get(hero_id)
    if hero:
        hero_dict = {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "powers": [{"id": power.id, "name": power.name, "description": power.description} for power in hero.powers]
        }
        return jsonify(hero_dict), 201
    else:
        return jsonify({"error": "Hero not found"}), 404

if __name__ == "__main__":
    app.run(port=5555, debug=True)
