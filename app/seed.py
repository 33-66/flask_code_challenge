from app import app, db
from models import Hero, Power, Hero_power


def seed_initial_data():
    with app.app_context():
        Hero.query.delete()
        Hero_power.query.delete()
        Power.query.delete()
        
        hero1 = Hero(name='Superman', super_name='Clark Kent')
        hero2 = Hero(name='Batman', super_name='Bruce Wayne')
        hero3 = Hero(name='Wax Man', super_name='Waxy')
        
        power1 = Power(name='Flight', description='Ability to fly through the air with great speed and agility, like a majestic bird in flight.')
        power2 = Power(name='Super Strength', description='Possesses immense physical strength, enabling feats of incredible power and force.')
        power3 = Power(name='Invisibility', description='Can become completely invisible to the naked eye, disappearing without a trace or detection.')

        hero2.hero_powers = [Hero_power(strength='Average', power=power2)]
        hero3.hero_powers = [Hero_power(strength='Average', power=power3)]

        db.session.add(hero1)
        db.session.add(hero2)
        db.session.add(hero3)
        db.session.add(power1)
        db.session.add(power2)
        db.session.add(power3)

        db.session.commit()


