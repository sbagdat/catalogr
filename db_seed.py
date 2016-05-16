from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

categories = [
    ['soccer',
        [{'name':'two shinguards',
           'description':'Description of two shinguards'},
          {'name':'shinguards',
           'description':'Description of singuards'},
          {'name':'jersey',
           'description':'Description of jersey'},
          {'name':'soccer cleats',
           'description':'Description of soccer cleats'}]],
    ['hockey',
        [{'name':'stick',
          'description':'Description of hockey stick'}]],
    ['snowboarding',
        [{'name':'goggles',
          'description':'Description of goggles'},
         {'name':'snowboard',
          'description':'Description of snowboard'}]],
    ['frisbee',
        [{'name':'frisbee',
          'description':'Description of frisbee'}]],
    ['baseball',
        [{'name':'bat',
          'description':'Description of bat'}]]
]

for category in categories:
    current_category = Category(name=category[0])
    session.add(current_category)
    session.commit()

    for item in category[1]:
        current_item = Item(name=item['name'],
                            description=item['description'],
                            category=current_category)
        session.add(current_item)
        session.commit()

print "Database seeding complete!"
