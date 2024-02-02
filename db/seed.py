from app.models import Hero, Power, HeroPower,db
def seed_data():
    # Create instances of the models with some sample data
    hero1 = Hero(name='Superman', super_name='Clark Kent')
    hero2 = Hero(name='Batman', super_name='Bruce Wayne')

    power1 = Power(name='Flight', description='Ability to fly')
    power2 = Power(name='Super Strength', description='Incredible strength')

    # Assign powers to heroes
    hero1.powers = [HeroPower(strength='High', power=power1)]
    hero2.powers = [HeroPower(strength='Very High', power=power2)]

    # Add the instances to the database session
    db.session.add(hero1)
    db.session.add(hero2)
    db.session.add(power1)
    db.session.add(power2)

    # Commit the changes to the database
    db.session.commit()