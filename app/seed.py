# seed.py
from app import app, db
from models import Hero, Power, Hero_power

def seed_data():
    with app.app_context():
        hero1 = Hero(name='Superman', super_name='Clark Kent')
        hero2 = Hero(name='Batman', super_name='Bruce Wayne')
        hero3 = Hero(name='wax man', super_name='waxy')
        power2 = Power(name='Super Strength', description='Incredible strength')
        power1 = Power(name='Flight', description='superpower  to fly like a bird')
        power3 = Power(name='Flight', description='superpower  to fly like a bird')
        
        hero2.hero_powers = [Hero_power(strength='Average', power=power2)]
        hero3.hero_powers = [Hero_power(strength='Average', power=power3)]

        db.session.add(hero1)
        db.session.add(hero2)
        db.session.add(hero3)
        db.session.add(power1)
        db.session.add(power2)
        db.session.add(power3)
        

        db.session.commit()

# Run the seed_data function to populate the database
seed_data()
