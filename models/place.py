#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from models.amenity import amenity


place_amenity = Table("place_amenity", Base.metadata,
        Column("place_id", ForeignKey("places.id")
            String(60), primary_key=True, nullable=False),
        Column("amenity_id", ForeignKey("amenities.id"),
            String(60), primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)


    storage_type = getenv('HBNB_TYPE_STORAGE')

    if storage_type == 'db':
        amenities = relationship("Amenity", secondary=place_amenity, viewonly=False)
    else:
        @property
        def amenities():
            '''
            Returns the list of `Amenity` instances
            based on the attribute `amenity_ids` that
            contains all `Amenity.id` linked to the Place
            '''
            return self.amenity_ids

        @amenities.setter
        def amenities(self, amenity_obj=None):
            '''
            handles append method for adding an
            Amenity.id to the attribute amenity_ids
            '''
            if type(amenity_obj) is Amenity and amenity_obj.id not in self.amenity_ids:
                self.amenity_ids.append(amenity_obj.id)
