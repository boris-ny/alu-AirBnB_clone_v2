#!/usr/bin/python3
"""Defines the database storage engine."""
from os import getenv
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """Represents a database storage engine.
    Attributes:
        __engine: SQLAlchemy engine.
        __session: SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects of a class"""
        classes = {
            'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        obj_dict = {}
        if cls is not None and cls in classes:
            class_objects = self.__session.query(classes[cls]).all()
            for obj in class_objects:
                key = obj.__class__.__name__ + "." + obj.id
                obj_dict[key] = obj

        if cls is None:
            for cls in classes:
                class_objects = self.__session.query(classes[cls]).all()
                for obj in class_objects:
                    key = obj.__class__.__name__ + "." + obj.id
                    obj_dict[key] = obj

        return obj_dict


    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        '''Delete from the current database session obj if not None.'''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):    
        """Close the working SQLAlchemy session."""
        self.__session.close()

