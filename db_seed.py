from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

categories = [
    ['soccer',
        [{'name':'Two Shinguards',
           'description':'Description of two shinguards',
           'price':'$3.99'},
          {'name':'Shinguards',
           'description':'Description of singuards',
           'price':'$5.99'},
          {'name':'Jersey',
           'description':'Description of jersey',
           'price':'$8.99'},
          {'name':'Soccer Cleats',
           'description':'Description of soccer cleats',
           'price':'$27.99'}]],
    ['hockey',
        [{'name':'Stick',
          'description':'Description of hockey stick',
         'price':'$5.99'}]],
    ['snowboarding',
        [{'name':'Goggles',
          'description':'Description of goggles',
          'price':'$12.99'},
         {'name':'Snowboard',
          'description':'Description of snowboard',
          'price':'$7.99'}]],
    ['frisbee',
        [{'name':'Frisbee',
          'description':'Description of frisbee',
          'price':'$32.99'}]],
    ['baseball',
        [{'name':'Bat',
          'description':'Description of bat',
          'price':'$4.99'}]]
]

for category in categories:
    current_category = Category(name=category[0])
    session.add(current_category)
    session.commit()

    for item in category[1]:
        current_item = Item(name=item['name'],
                            description=item['description'],
                            price=item['price'],
                            category=current_category)
        session.add(current_item)
        session.commit()

print "Database seeding complete!"
